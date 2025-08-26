# -*- coding: utf-8 -*-
"""
Voice Activity Detection Interface for Mojio
Mojio 音声区間検出インターフェース

音声区間検出機能の抽象インターフェース定義
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple


class VoiceActivityDetectionInterface(ABC):
    """
    音声区間検出機能の抽象インターフェース
    
    さまざまなVAD実装を統一的に扱うためのインターフェース
    """
    
    @abstractmethod
    def initialize(self, sample_rate: int = 16000) -> None:
        """
        VADモデルを初期化する
        
        Args:
            sample_rate: サンプリングレート (Hz)
        """
        pass
    
    @abstractmethod
    def is_speech(self, audio_data: np.ndarray) -> bool:
        """
        音声データに音声が含まれているか判定する
        
        Args:
            audio_data: 音声データ (numpy配列)
            
        Returns:
            bool: 音声が含まれている場合はTrue、そうでない場合はFalse
        """
        pass
    
    @abstractmethod
    def detect_speech_segments(self, audio_data: np.ndarray) -> list:
        """
        音声データから音声区間を検出する
        
        Args:
            audio_data: 音声データ (numpy配列)
            
        Returns:
            list: 音声区間のリスト [(start_time, end_time), ...]
        """
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """
        VADの内部状態をリセットする
        """
        pass