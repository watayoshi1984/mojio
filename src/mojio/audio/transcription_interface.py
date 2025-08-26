# -*- coding: utf-8 -*-
"""
Speech Recognition Interface for Mojio
Mojio 音声認識インターフェース

音声認識エンジンへの抽象化インターフェース
"""

from abc import ABC, abstractmethod
from typing import Optional, Callable, List
import numpy as np


class SpeechRecognitionInterface(ABC):
    """
    音声認識エンジンの抽象化インターフェース
    
    各種音声認識エンジン（Whisper, Google Speech-to-Text等）の
    共通インターフェースを定義
    """
    
    @abstractmethod
    def initialize(self, 
                  model_size: str = "large-v2",
                  device: str = "auto",
                  compute_type: str = "float16") -> None:
        """
        音声認識エンジンを初期化
        
        Args:
            model_size: モデルサイズ ("tiny", "base", "small", "medium", "large-v2")
            device: 実行デバイス ("cpu", "cuda", "auto")
            compute_type: 計算精度 ("float16", "float32", "int8")
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def is_initialized(self) -> bool:
        """
        音声認識エンジンが初期化されているかを返す
        
        Returns:
            bool: 初期化済みならTrue
        """
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """
        サポートする言語一覧を取得
        
        Returns:
            List[str]: 言語コードのリスト
        """
        pass


# 認識結果の型定義
TranscriptionResult = dict[str, str | float | dict]