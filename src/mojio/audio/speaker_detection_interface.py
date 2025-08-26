# -*- coding: utf-8 -*-
"""
Speaker Detection Interface for Mojio
Mojio 話者検出インターフェース

話者検出の抽象インターフェース定義
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import List, Tuple, Optional


class SpeakerDetectionInterface(ABC):
    """
    話者検出の抽象インターフェース
    
    さまざまな話者検出実装を統一的に扱うためのインターフェース
    """
    
    @abstractmethod
    def initialize(self, **kwargs) -> None:
        """
        話者検出を初期化する
        
        Args:
            **kwargs: 初期化パラメータ
        """
        pass
    
    @abstractmethod
    def detect_speaker_change(self, audio_data: np.ndarray) -> bool:
        """
        音声データから話者切り替えを検出する
        
        Args:
            audio_data: 音声データ（numpy配列）
            
        Returns:
            bool: 話者切り替えが検出された場合はTrue、そうでない場合はFalse
        """
        pass
    
    @abstractmethod
    def get_speaker_features(self, audio_data: np.ndarray) -> List[float]:
        """
        音声データから話者の特徴量を抽出する
        
        Args:
            audio_data: 音声データ（numpy配列）
            
        Returns:
            List[float]: 話者の特徴量
        """
        pass
    
    @abstractmethod
    def is_initialized(self) -> bool:
        """
        話者検出が初期化されているかを返す
        
        Returns:
            bool: 初期化済みならTrue
        """
        pass