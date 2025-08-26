# -*- coding: utf-8 -*-
"""
Audio Input Manager for Mojio
Mojio 音声入力管理

マイクとループバック音声の統合管理クラス
"""

from typing import Optional, Callable, List
import numpy as np
import gc
from .audio_input_interface import AudioDeviceInfo
from .microphone_input import MicrophoneAudioInput
from .loopback_input import LoopbackAudioInput


class AudioInputManager:
    """
    音声入力の統合管理クラス
    
    マイク入力とループバック入力の両方を管理し、
    統一されたインターフェースで音声データを提供
    """
    
    def __init__(self):
        """音声入力管理を初期化"""
        self.microphone_input = MicrophoneAudioInput()
        self.loopback_input = LoopbackAudioInput()
        self.current_input_type: Optional[str] = None  # "microphone" or "loopback"
        self.is_active: bool = False
        self.callback_func: Optional[Callable[[np.ndarray], None]] = None
        
    def initialize(self) -> None:
        """
        音声入力管理を初期化する
        """
        # 現在の実装では特別な初期化は不要
        # 必要に応じて追加の初期化処理をここに記述
        pass
        
    def get_microphone_devices(self) -> List[AudioDeviceInfo]:
        """
        マイクデバイス一覧を取得
        
        Returns:
            List[dict]: マイクデバイス情報のリスト
        """
        return self.microphone_input.get_device_list()
    
    def get_loopback_devices(self) -> List[AudioDeviceInfo]:
        """
        ループバックデバイス一覧を取得
        
        Returns:
            List[dict]: ループバックデバイス情報のリスト
        """
        return self.loopback_input.get_device_list()
    
    def open_microphone_stream(self, 
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
        self.microphone_input.open_stream(device_id, sample_rate, channels, buffer_size)
        self.current_input_type = "microphone"
        
    def open_loopback_stream(self, 
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
        self.loopback_input.open_stream(device_id, sample_rate, channels, buffer_size)
        self.current_input_type = "loopback"
        
    def close_stream(self) -> None:
        """現在の音声ストリームを閉じる"""
        if self.current_input_type == "microphone":
            self.microphone_input.close_stream()
        elif self.current_input_type == "loopback":
            self.loopback_input.close_stream()
        self.current_input_type = None
        self.is_active = False
        
    def start_stream(self, callback: Callable[[np.ndarray], None]) -> None:
        """
        音声ストリームの読み取りを開始
        
        Args:
            callback: 音声データ受信時のコールバック関数
        """
        # コールバック関数をラップしてメモリ管理を追加
        def wrapped_callback(audio_data: np.ndarray) -> None:
            try:
                callback(audio_data)
            finally:
                # コールバック実行後に音声データのメモリを解放
                del audio_data
                gc.collect()
                
        self.callback_func = wrapped_callback
        
        if self.current_input_type == "microphone":
            self.microphone_input.start_stream(wrapped_callback)
        elif self.current_input_type == "loopback":
            self.loopback_input.start_stream(wrapped_callback)
            
        self.is_active = True
    
    def stop_stream(self) -> None:
        """音声ストリームの読み取りを停止"""
        if self.current_input_type == "microphone":
            self.microphone_input.stop_stream()
        elif self.current_input_type == "loopback":
            self.loopback_input.stop_stream()
            
        self.is_active = False
    
    def is_stream_active(self) -> bool:
        """
        音声ストリームがアクティブかどうかを返す
        
        Returns:
            bool: ストリームがアクティブならTrue
        """
        if self.current_input_type == "microphone":
            return self.microphone_input.is_stream_active()
        elif self.current_input_type == "loopback":
            return self.loopback_input.is_stream_active()
        return False
    
    def switch_input_type(self, input_type: str) -> None:
        """
        音声入力の種類を切り替える
        
        Args:
            input_type: 入力種類（"microphone" or "loopback"）
        """
        if input_type not in ["microphone", "loopback"]:
            raise ValueError("input_typeは'microphone'または'loopback'である必要があります")
            
        # 現在アクティブな場合は停止
        if self.is_active:
            self.stop_stream()
            
        # ストリームを閉じる
        self.close_stream()
        
        # 入力タイプを更新
        self.current_input_type = input_type


# テスト用の簡単な使用例
if __name__ == "__main__":
    import time
    
    def test_callback(audio_data: np.ndarray):
        """テスト用コールバック関数"""
        # 音声レベルを計算して表示
        level = np.sqrt(np.mean(audio_data**2))
        print(f"音声レベル: {level:.4f}")
    
    # 音声入力管理のテスト
    audio_manager = AudioInputManager()
    
    try:
        # マイクデバイスを表示
        mic_devices = audio_manager.get_microphone_devices()
        print("マイクデバイス:")
        for device in mic_devices:
            print(f"  ID: {device['id']}, 名前: {device['name']}")
            
        # ループバックデバイスを表示
        loopback_devices = audio_manager.get_loopback_devices()
        print("\nループバックデバイス:")
        for device in loopback_devices:
            print(f"  ID: {device['id']}, 名前: {device['name']}")
            
        # マイク入力をテスト
        if mic_devices:
            print("\nマイク入力テストを開始します...")
            audio_manager.open_microphone_stream(
                device_id=mic_devices[0]['id'],
                sample_rate=16000,
                channels=1,
                buffer_size=1024
            )
            
            audio_manager.start_stream(test_callback)
            print("マイク音声キャプチャを開始しました。3秒間テストします...")
            time.sleep(3)
            audio_manager.stop_stream()
            audio_manager.close_stream()