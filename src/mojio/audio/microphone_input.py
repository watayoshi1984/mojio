# -*- coding: utf-8 -*-
"""
Microphone Audio Input Implementation for Mojio
Mojio マイク音声入力実装

SoundDeviceを使用したマイク音声入力の具体実装
"""

import sounddevice as sd
import numpy as np
from typing import List, Optional, Callable
from .audio_input_interface import AudioInputInterface, AudioDeviceInfo


class MicrophoneAudioInput(AudioInputInterface):
    """
    SoundDeviceを使用したマイク音声入力実装
    
    マイクからの音声をキャプチャし、
    リアルタイムで処理するためのクラス
    """
    
    def __init__(self):
        """マイク音声入力を初期化"""
        self.device_id: Optional[int] = None
        self.sample_rate: int = 16000
        self.channels: int = 1
        self.buffer_size: int = 1024
        self.stream: Optional[sd.InputStream] = None
        self.callback_func: Optional[Callable[[np.ndarray], None]] = None
        
    def get_device_list(self) -> List[AudioDeviceInfo]:
        """
        利用可能なマイクデバイス一覧を取得
        
        Returns:
            List[dict]: マイクデバイス情報のリスト
        """
        devices = sd.query_devices()
        input_devices = []
        
        for i, device in enumerate(devices):
            # 入力チャンネルを持つデバイスのみを抽出
            if device['max_input_channels'] > 0:
                device_info: AudioDeviceInfo = {
                    'id': i,
                    'name': device['name'],
                    'max_input_channels': device['max_input_channels'],
                    'default_samplerate': device['default_samplerate']
                }
                input_devices.append(device_info)
                
        return input_devices
    
    def open_stream(self, 
                   device_id: Optional[int] = None,
                   sample_rate: int = 16000,
                   channels: int = 1,
                   buffer_size: int = 1024) -> None:
        """
        マイク音声ストリームを開く
        
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
            self.device_id = sd.default.device[0]  # デフォルト入力デバイス
            
        # InputStreamを作成
        self.stream = sd.InputStream(
            device=self.device_id,
            channels=self.channels,
            samplerate=self.sample_rate,
            blocksize=self.buffer_size,
            dtype='float32'
        )
    
    def close_stream(self) -> None:
        """マイク音声ストリームを閉じる"""
        if self.stream is not None:
            if self.stream.active:
                self.stream.stop()
            self.stream.close()
            self.stream = None
            
    def start_stream(self, callback: Callable[[np.ndarray], None]) -> None:
        """
        マイク音声ストリームの読み取りを開始
        
        Args:
            callback: 音声データ受信時のコールバック関数
        """
        if self.stream is None:
            raise RuntimeError("ストリームが開かれていません。open_stream()を先に呼び出してください。")
            
        self.callback_func = callback
        self.stream.start()
        
        # コールバック関数を設定
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"音声ストリームステータス: {status}")
            if self.callback_func is not None:
                # indataは3次元配列（frames, channels, 1）なので2次元に変換
                audio_data = indata[:, 0]  # モノラルの場合、最初のチャンネルのみ使用
                self.callback_func(audio_data)
                
        self.stream.callback = audio_callback
    
    def stop_stream(self) -> None:
        """マイク音声ストリームの読み取りを停止"""
        if self.stream is not None and self.stream.active:
            self.stream.stop()
            
    def is_stream_active(self) -> bool:
        """
        マイク音声ストリームがアクティブかどうかを返す
        
        Returns:
            bool: ストリームがアクティブならTrue
        """
        if self.stream is None:
            return False
        return self.stream.active


# テスト用の簡単な使用例
if __name__ == "__main__":
    import time
    
    def test_callback(audio_data: np.ndarray):
        """テスト用コールバック関数"""
        # 音声レベルを計算して表示
        level = np.sqrt(np.mean(audio_data**2))
        print(f"音声レベル: {level:.4f}")
    
    # マイク入力のテスト
    mic_input = MicrophoneAudioInput()
    
    try:
        # 利用可能なデバイスを表示
        devices = mic_input.get_device_list()
        print("利用可能なマイクデバイス:")
        for device in devices:
            print(f"  ID: {device['id']}, 名前: {device['name']}")
            
        # 最初のデバイスを使用してストリームを開く
        if devices:
            mic_input.open_stream(
                device_id=devices[0]['id'],
                sample_rate=16000,
                channels=1,
                buffer_size=1024
            )
            
            # ストリームを開始
            mic_input.start_stream(test_callback)
            print("マイク音声キャプチャを開始しました。5秒間テストします...")
            
            # 5秒間テスト
            time.sleep(5)
            
            # ストリームを停止
            mic_input.stop_stream()
            print("マイク音声キャプチャを停止しました。")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        # ストリームを閉じる
        mic_input.close_stream()