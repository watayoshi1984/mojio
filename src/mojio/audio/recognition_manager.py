# -*- coding: utf-8 -*-
"""
Speech Recognition Manager for Mojio
Mojio 音声認識管理

音声認識エンジンの統合管理クラス
"""

from typing import Optional, Callable
import numpy as np
from .transcription_interface import SpeechRecognitionInterface
from .whisper_recognition import WhisperSpeechRecognition


class SpeechRecognitionManager:
    """
    音声認識エンジンの統合管理クラス
    
    複数の音声認識エンジンを管理し、
    統一されたインターフェースで音声認識機能を提供
    """
    
    def __init__(self):
        """音声認識管理を初期化"""
        self.whisper_recognition = WhisperSpeechRecognition()
        self.current_engine: Optional[SpeechRecognitionInterface] = None
        self.current_engine_type: Optional[str] = None
        self.is_active: bool = False
        
    def initialize_engine(self, 
                         engine_type: str = "whisper",
                         **kwargs) -> None:
        """
        音声認識エンジンを初期化
        
        Args:
            engine_type: エンジンタイプ ("whisper")
            **kwargs: エンジン固有の初期化パラメータ
        """
        if engine_type == "whisper":
            # Whisperエンジンを初期化
            model_size = kwargs.get("model_size", "large-v2")
            device = kwargs.get("device", "auto")
            compute_type = kwargs.get("compute_type", "float16")
            
            self.whisper_recognition.initialize(
                model_size=model_size,
                device=device,
                compute_type=compute_type
            )
            
            self.current_engine = self.whisper_recognition
            self.current_engine_type = "whisper"
        else:
            raise ValueError(f"サポートされていないエンジンタイプ: {engine_type}")
        
        self.is_active = True
    
    def transcribe(self, 
                  audio_data: np.ndarray,
                  language: Optional[str] = None) -> str:
        """
        音声データをテキストに変換
        
        Args:
            audio_data: 音声データ（numpy配列）
            language: 言語コード（Noneの場合は自動検出）
            
        Returns:
            str: 認識結果のテキスト
        """
        if not self.is_active or self.current_engine is None:
            raise RuntimeError("音声認識エンジンが初期化されていません。")
            
        return self.current_engine.transcribe(audio_data, language)
    
    def transcribe_stream(self, 
                         audio_stream: Callable[[], np.ndarray],
                         language: Optional[str] = None,
                         callback: Optional[Callable[[str], None]] = None) -> None:
        """
        ストリーム音声データをリアルタイムにテキストに変換
        
        Args:
            audio_stream: 音声データを返すコールバック関数
            language: 言語コード（Noneの場合は自動検出）
            callback: 認識結果受信時のコールバック関数
        """
        if not self.is_active or self.current_engine is None:
            raise RuntimeError("音声認識エンジンが初期化されていません。")
            
        self.current_engine.transcribe_stream(audio_stream, language, callback)
    
    def is_engine_initialized(self) -> bool:
        """
        音声認識エンジンが初期化されているかを返す
        
        Returns:
            bool: 初期化済みならTrue
        """
        if self.current_engine is None:
            return False
        return self.current_engine.is_initialized()
    
    def get_supported_languages(self) -> list:
        """
        サポートする言語一覧を取得
        
        Returns:
            list: 言語コードのリスト
        """
        if self.current_engine is None:
            return []
        return self.current_engine.get_supported_languages()
    
    def switch_engine(self, engine_type: str, **kwargs) -> None:
        """
        音声認識エンジンを切り替える
        
        Args:
            engine_type: エンジンタイプ ("whisper")
            **kwargs: エンジン固有の初期化パラメータ
        """
        # 現在アクティブな場合は停止
        self.is_active = False
        
        # エンジンを切り替え
        self.initialize_engine(engine_type, **kwargs)


# テスト用の簡単な使用例
if __name__ == "__main__":
    import time
    
    def generate_dummy_audio() -> np.ndarray:
        """テスト用のダミー音声データを生成"""
        # 1秒分の無音データ（16kHz, モノラル）
        return np.zeros(16000, dtype=np.float32)
    
    # 音声認識管理のテスト
    recognition_manager = SpeechRecognitionManager()
    
    try:
        # Whisperエンジンを初期化
        print("Whisperエンジンを初期化中...")
        recognition_manager.initialize_engine(
            engine_type="whisper",
            model_size="tiny",
            device="cpu",
            compute_type="float32"
        )
        
        if recognition_manager.is_engine_initialized():
            print("Whisperエンジンの初期化に成功しました。")
            
            # ダミー音声データでテスト
            dummy_audio = generate_dummy_audio()
            print("ダミー音声データで音声認識をテスト中...")
            
            result = recognition_manager.transcribe(dummy_audio, language="ja")
            print(f"認識結果: {result}")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")