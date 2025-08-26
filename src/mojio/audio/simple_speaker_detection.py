# -*- coding: utf-8 -*-
"""
Simple Speaker Detection Implementation for Mojio
Mojio 簡易話者検出実装

音声のエネルギー変化を検出して話者切り替えを検出する
"""

import numpy as np
from typing import List
from .speaker_detection_interface import SpeakerDetectionInterface


class SimpleSpeakerDetection(SpeakerDetectionInterface):
    """
    簡易話者検出の具体実装
    
    音声のエネルギー（音量）の変化を検出して
    話者切り替えを検出する機能を提供する
    """
    
    def __init__(self):
        """簡易話者検出を初期化"""
        self.is_active = False
        self.energy_threshold = 0.01  # エネルギー閾値
        self.silence_threshold = 0.005  # 無音閾値
        self.silence_duration = 0.5  # 無音と判定する時間（秒）
        self.sample_rate = 16000  # サンプリングレート
        self.silence_counter = 0  # 無音カウンター
        self.last_energy = 0.0  # 前回のエネルギー
        self.energy_change_threshold = 0.02  # エネルギー変化閾値
        
    def initialize(self, energy_threshold: float = 0.01, silence_threshold: float = 0.005, 
                  silence_duration: float = 0.5, sample_rate: int = 16000) -> None:
        """
        簡易話者検出を初期化する
        
        Args:
            energy_threshold: エネルギー閾値
            silence_threshold: 無音閾値
            silence_duration: 無音と判定する時間（秒）
            sample_rate: サンプリングレート
        """
        self.energy_threshold = energy_threshold
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.sample_rate = sample_rate
        self.silence_counter = 0
        self.last_energy = 0.0
        self.is_active = True
        
    def detect_speaker_change(self, audio_data: np.ndarray) -> bool:
        """
        音声データから話者切り替えを検出する
        
        Args:
            audio_data: 音声データ（numpy配列）
            
        Returns:
            bool: 話者切り替えが検出された場合はTrue、そうでない場合はFalse
        """
        if not self.is_active:
            return False
            
        # 音声エネルギーを計算
        energy = self._calculate_energy(audio_data)
        
        # 無音カウンターを更新
        if energy < self.silence_threshold:
            self.silence_counter += len(audio_data) / self.sample_rate
        else:
            self.silence_counter = 0
            
        # エネルギーの変化が閾値を超えた場合、話者切り替えと判定
        energy_change = abs(energy - self.last_energy)
        self.last_energy = energy
        
        # 無音時間が一定以上で、エネルギーの変化が閾値を超えた場合に話者切り替えと判定
        if self.silence_counter >= self.silence_duration and energy_change >= self.energy_change_threshold:
            self.silence_counter = 0  # カウンターをリセット
            return True
            
        return False
    
    def get_speaker_features(self, audio_data: np.ndarray) -> List[float]:
        """
        音声データから話者の特徴量を抽出する
        
        Args:
            audio_data: 音声データ（numpy配列）
            
        Returns:
            List[float]: 話者の特徴量（エネルギー、ゼロクロス率など）
        """
        if not self.is_active:
            return []
            
        # エネルギーを計算
        energy = self._calculate_energy(audio_data)
        
        # ゼロクロス率を計算
        zero_crossing_rate = self._calculate_zero_crossing_rate(audio_data)
        
        return [energy, zero_crossing_rate]
    
    def is_initialized(self) -> bool:
        """
        話者検出が初期化されているかを返す
        
        Returns:
            bool: 初期化済みならTrue
        """
        return self.is_active
    
    def _calculate_energy(self, audio_data: np.ndarray) -> float:
        """
        音声データのエネルギーを計算する
        
        Args:
            audio_data: 音声データ（numpy配列）
            
        Returns:
            float: エネルギー
        """
        return float(np.sqrt(np.mean(audio_data**2)))
    
    def _calculate_zero_crossing_rate(self, audio_data: np.ndarray) -> float:
        """
        音声データのゼロクロス率を計算する
        
        Args:
            audio_data: 音声データ（numpy配列）
            
        Returns:
            float: ゼロクロス率
        """
        # 符号が変わった回数をカウント
        zero_crossings = np.sum(np.diff(np.sign(audio_data)) != 0)
        # 総サンプル数で割ってゼロクロス率を計算
        return float(zero_crossings / len(audio_data))