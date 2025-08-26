# -*- coding: utf-8 -*-
"""
Noise Reduction Manager for Mojio
Mojio ノイズ除去管理

ノイズ除去機能の統合管理クラス
"""

from typing import Optional, Dict, Any
import numpy as np
from .noise_reduction_interface import NoiseReductionInterface
from .noise_reduction import SpectralGatingNoiseReduction
from .deep_learning_noise_reduction import DeepLearningNoiseReduction


class NoiseReductionManager:
    """
    ノイズ除去機能の統合管理クラス
    
    さまざまなノイズ除去アルゴリズムの統合管理と
    簡単な使用方法を提供する
    """
    
    def __init__(self):
        """ノイズ除去管理を初期化"""
        self.noise_reducer: Optional[NoiseReductionInterface] = None
        self.is_initialized: bool = False
        self.current_algorithm: Optional[str] = None
        
    def initialize(self, algorithm: str = "spectral_gating", sample_rate: int = 16000, **kwargs) -> None:
        """
        ノイズ除去管理を初期化する
        
        Args:
            algorithm: 使用するノイズ除去アルゴリズム（デフォルト: "spectral_gating"）
            sample_rate: サンプリングレート（デフォルト: 16000）
            **kwargs: アルゴリズム固有の初期化パラメータ
        """
        # アルゴリズムに応じてノイズ除去オブジェクトを作成
        if algorithm == "spectral_gating":
            self.noise_reducer = SpectralGatingNoiseReduction()
        elif algorithm == "deep_learning":
            self.noise_reducer = DeepLearningNoiseReduction()
        else:
            raise ValueError(f"サポートされていないノイズ除去アルゴリズム: {algorithm}")
            
        # ノイズ除去オブジェクトを初期化
        self.noise_reducer.initialize(sample_rate, **kwargs)
        
        self.current_algorithm = algorithm
        self.is_initialized = True
        
    def reduce_noise(self, audio_data: np.ndarray) -> np.ndarray:
        """
        音声データからノイズを除去する
        
        Args:
            audio_data: 入力音声データ (numpy配列)
            
        Returns:
            np.ndarray: ノイズ除去後の音声データ
            
        Raises:
            RuntimeError: ノイズ除去管理が初期化されていない場合
        """
        if not self.is_initialized:
            raise RuntimeError("ノイズ除去管理が初期化されていません。initialize()を先に呼び出してください。")
            
        return self.noise_reducer.reduce_noise(audio_data)
        
    def reset(self) -> None:
        """
        ノイズ除去機能の状態をリセットする
        """
        if self.is_initialized:
            self.noise_reducer.reset()