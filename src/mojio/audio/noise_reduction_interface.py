# -*- coding: utf-8 -*-
"""
Noise Reduction Interface for Mojio
Mojio ノイズ除去インターフェース

音声データのノイズ除去機能の抽象インターフェース
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Any


class NoiseReductionInterface(ABC):
    """
    ノイズ除去機能の抽象インターフェースクラス
    
    さまざまなノイズ除去アルゴリズムの共通インターフェースを定義する
    """
    
    @abstractmethod
    def initialize(self, sample_rate: int, **kwargs) -> None:
        """
        ノイズ除去機能を初期化する
        
        Args:
            sample_rate: サンプリングレート
            **kwargs: その他の初期化パラメータ
        """
        pass
        
    @abstractmethod
    def reduce_noise(self, audio_data: np.ndarray) -> np.ndarray:
        """
        音声データからノイズを除去する
        
        Args:
            audio_data: 入力音声データ (numpy配列)
            
        Returns:
            np.ndarray: ノイズ除去後の音声データ
        """
        pass
        
    @abstractmethod
    def reset(self) -> None:
        """
        ノイズ除去機能の状態をリセットする
        """
        pass