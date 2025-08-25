# -*- coding: utf-8 -*-
"""
Loopback Audio Input Implementation for Mojio
Mojio ループバック音声入力実装

SoundCardを使用したPC内部音声（ループバック録音）の具体実装
"""

import soundcard as sc
import numpy as np
from typing import List, Optional, Callable
from .audio_input_interface import AudioInputInterface, AudioDeviceInfo


class LoopbackAudioInput(AudioInputInterface):
    """
    SoundCardを使用したループバック音声入力実装
    
    PC上で再生されている音声（オンライン会議の相手の声など）を
    キャプチャするためのクラス
    """
    
    def __init__(self):
        """ループバック音声入力を初期化"""
        self.device_id: Optional[str] = None
        self.sample_rate: int = 16000
        self.channels: int = 1
        self.buffer_size: int = 1024
        self.microphone: Optional[sc.Microphone] = None
        self.recorder: Optional[sc.Recorder] = None
        self.callback_func: Optional[Callable[[np.ndarray], None]] = None
        self.is_recording: bool = False
        
    def get_device_list(self) -> List[AudioDeviceInfo]:
        """
        利用可能なループバックデバイス一覧を取得
        
        Returns:
            List[dict]: ループバックデバイス情報のリスト
        """
        speakers = sc.all_speakers()
        loopback_devices = []
        
        for i, speaker in enumerate(speakers):
            device_info: AudioDeviceInfo = {
                'id': speaker.id,  # SoundCardでは文字列IDを使用
                'name': speaker.name,
                'max_input_channels': speaker.channels,
                'default_samplerate': 48000  # SoundCardのデフォルト
            }
            loopback_devices.append(device_info)
                
        return loopback_devices
    
    def open_stream(self, 
                   device_id: Optional[str] = None,
                   sample_rate: int = 16000,
                   channels: int = 1,
                   buffer_size: int = 1024) -> None:
        """
        ループバック音声ストリームを開く
        
        Args:
            device_id: デバイスID（Noneの場合はデフォルトデバイス）
            sample_rate: サンプリングレート（Hz）
            channels: チャンネル数
            buffer_size: バッファサイズ（フレーム数）
        """
        self.device_id = device_id
        self.sample_rate = sample_rate
        self.channels = channels
        self.buffer_size = buffer_size
        
        # デバイスIDが指定されていない場合はデフォルトデバイスを使用
        if self.device_id is None:
            default_speaker = sc.default_speaker()
            self.device_id = default_speaker.id
            
        # マイクオブジェクトを作成
        self.microphone = sc.get_microphone(self.device_id, include_loopback=True)
        
        # レコーダーを作成
        self.recorder = self.microphone.recorder(
            samplerate=self.sample_rate,
            channels=self.channels,
            blocksize=self.buffer_size
        )
    
    def close_stream(self) -> None:
        """ループバック音声ストリームを閉じる"""
        self.is_recording = False
        if self.recorder is not None:
            # Recorderはコンテキストマネージャーなので特別なクローズ処理は不要
            self.recorder = None
        if self.microphone is not None:
            self.microphone = None
            
    def start_stream(self, callback: Callable[[np.ndarray], None]) -> None:
        """
        ループバック音声ストリームの読み取りを開始
        
        Args:
            callback: 音声データ受信時のコールバック関数
        """
        if self.recorder is None:
            raise RuntimeError("ストリームが開かれていません。open_stream()を先に呼び出してください。")
            
        self.callback_func = callback
        self.is_recording = True
        
        # 非同期で録音を開始
        import threading
        
        def record_loop():
            try:
                with self.recorder as recorder:
                    while self.is_recording:
                        # 音声データを読み取り
                        data = recorder.record(numframes=self.buffer_size)
                        # dataは3次元配列（frames, channels, 1）なので2次元に変換
                        if data.shape[1] >= 1:
                            audio_data = data[:, 0]  # モノラルの場合、最初のチャンネルのみ使用
                            if self.callback_func is not None:
                                self.callback_func(audio_data)
            except Exception as e:
                print(f"ループバック録音エラー: {e}")
                self.is_recording = False
                
        # 録音スレッドを開始
        record_thread = threading.Thread(target=record_loop, daemon=True)
        record_thread.start()
    
    def stop_stream(self) -> None:
        """ループバック音声ストリームの読み取りを停止"""
        self.is_recording = False
            
    def is_stream_active(self) -> bool:
        """
        ループバック音声ストリームがアクティブかどうかを返す
        
        Returns:
            bool: ストリームがアクティブならTrue
        """
        return self.is_recording


# テスト用の簡単な使用例
if __name__ == "__main__":
    import time
    
    def test_callback(audio_data: np.ndarray):
        """テスト用コールバック関数"""
        # 音声レベルを計算して表示
        level = np.sqrt(np.mean(audio_data**2))
        print(f"ループバック音声レベル: {level:.4f}")
    
    # ループバック入力のテスト
    loopback_input = LoopbackAudioInput()
    
    try:
        # 利用可能なデバイスを表示
        devices = loopback_input.get_device_list()
        print("利用可能なループバックデバイス:")
        for device in devices:
            print(f"  ID: {device['id']}, 名前: {device['name']}")
            
        # 最初のデバイスを使用してストリームを開く
        if devices:
            loopback_input.open_stream(
                device_id=devices[0]['id'],
                sample_rate=16000,
                channels=1,
                buffer_size=1024
            )
            
            # ストリームを開始
            loopback_input.start_stream(test_callback)
            print("ループバック音声キャプチャを開始しました。5秒間テストします...")
            
            # 5秒間テスト
            time.sleep(5)
            
            # ストリームを停止
            loopback_input.stop_stream()
            print("ループバック音声キャプチャを停止しました。")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        # ストリームを閉じる
        loopback_input.close_stream()