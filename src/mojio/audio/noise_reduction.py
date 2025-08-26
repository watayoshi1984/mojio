# -*- coding: utf-8 -*-
"""
Noise Reduction Implementation for Mojio
Mojio ノイズ除去実装

noisereduceライブラリを使用したノイズ除去機能の具体実装
"""

import numpy as np
import noisereduce as nr
from typing import Optional
from .noise_reduction_interface import NoiseReductionInterface


class SpectralGatingNoiseReduction(NoiseReductionInterface):
    """
    スペクトルゲート方式のノイズ除去クラス
    
    noisereduceライブラリを使用してスペクトルゲート方式の
    ノイズ除去機能を提供する
    """
    
    def __init__(self):
        """スペクトルゲート方式のノイズ除去を初期化"""
        self.sample_rate: Optional[int] = None
        self.is_initialized: bool = False
        
    def initialize(self, sample_rate: int, **kwargs) -> None:
        """
        スペクトルゲート方式のノイズ除去を初期化する
        
        Args:
            sample_rate: サンプリングレート
            **kwargs: その他の初期化パラメータ
                - n_fft: FFTのポイント数（デフォルト: 512）
                - hop_length: ホップ長（デフォルト: 256）
                - win_length: ウィンドウ長（デフォルト: 512）
                - time_constant_s: 時間定数（秒）（デフォルト: 2.0）
                - freq_mask_smooth_hz: 周波数マスクのスムージング（Hz）（デフォルト: 500）
                - time_mask_smooth_ms: 時間マスクのスムージング（ms）（デフォルト: 50）
        """
        self.sample_rate = sample_rate
        
        # その他のパラメータを設定
        self.n_fft = kwargs.get('n_fft', 512)
        self.hop_length = kwargs.get('hop_length', 256)
        self.win_length = kwargs.get('win_length', 512)
        self.time_constant_s = kwargs.get('time_constant_s', 2.0)
        self.freq_mask_smooth_hz = kwargs.get('freq_mask_smooth_hz', 500)
        self.time_mask_smooth_ms = kwargs.get('time_mask_smooth_ms', 50)
        
        self.is_initialized = True
        
    def reduce_noise(self, audio_data: np.ndarray) -> np.ndarray:
        """
        音声データからノイズを除去する
        
        Args:
            audio_data: 入力音声データ (numpy配列)
            
        Returns:
            np.ndarray: ノイズ除去後の音声データ
            
        Raises:
            RuntimeError: ノイズ除去機能が初期化されていない場合
        """
        if not self.is_initialized:
            raise RuntimeError("ノイズ除去機能が初期化されていません。initialize()を先に呼び出してください。")
            
        # noisereduceを使用してノイズを除去
        reduced_noise = nr.reduce_noise(
            y=audio_data,
            sr=self.sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            win_length=self.win_length,
            time_constant_s=self.time_constant_s,
            freq_mask_smooth_hz=self.freq_mask_smooth_hz,
            time_mask_smooth_ms=self.time_mask_smooth_ms
        )
        
        return reduced_noise
        
    def reset(self) -> None:
        """
        スペクトルゲート方式のノイズ除去の状態をリセットする
        """
        pass