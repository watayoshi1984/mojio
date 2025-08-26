# -*- coding: utf-8 -*-
"""
Speaker Detection Manager for Mojio
Mojio 話者検出管理

話者検出機能の統合管理クラス
"""

from typing import Optional
import numpy as np
from .speaker_detection_interface import SpeakerDetectionInterface
from .simple_speaker_detection import SimpleSpeakerDetection


class SpeakerDetectionManager:
    """
    話者検出機能の統合管理クラス
    
    さまざまな話者検出実装を統一的に管理し、
    アプリケーション全体から簡単に利用できるようにする
    """
    
    def __init__(self):
        """話者検出管理クラスを初期化"""
        self.simple_detection = SimpleSpeakerDetection()
        self.current_detector: Optional[SpeakerDetectionInterface] = None
        self.current_detector_type: Optional[str] = None
        self.is_active = False
        
    def initialize_detector(self, detector_type: str = "simple", **kwargs) -> None:
        """
        話者検出器を初期化する
        
        Args:
            detector_type: 検出器タイプ ("simple" など)
            **kwargs: 検出器固有の初期化パラメータ
        """
        if detector_type == "simple":
            self.simple_detection.initialize(**kwargs)
            self.current_detector = self.simple_detection
            self.current_detector_type = detector_type
        else:
            raise ValueError(f"サポートされていない検出器タイプ: {detector_type}")
            
        self.is_active = True
        
    def detect_speaker_change(self, audio_data: np.ndarray) -> bool:
        """
        音声データから話者切り替えを検出する
        
        Args:
            audio_data: 音声データ（numpy配列）
            
        Returns:
            bool: 話者切り替えが検出された場合はTrue、そうでない場合はFalse
        """
        if not self.is_active or self.current_detector is None:
            return False
            
        return self.current_detector.detect_speaker_change(audio_data)
    
    def get_speaker_features(self, audio_data: np.ndarray) -> list:
        """
        音声データから話者の特徴量を抽出する
        
        Args:
            audio_data: 音声データ（numpy配列）
            
        Returns:
            list: 話者の特徴量
        """
        if not self.is_active or self.current_detector is None:
            return []
            
        return self.current_detector.get_speaker_features(audio_data)
    
    def is_detector_initialized(self) -> bool:
        """
        話者検出器が初期化されているかを返す
        
        Returns:
            bool: 初期化済みならTrue
        """
        if self.current_detector is None:
            return False
        return self.current_detector.is_initialized()
    
    def switch_detector(self, detector_type: str, **kwargs) -> None:
        """
        話者検出器を切り替える
        
        Args:
            detector_type: 検出器タイプ ("simple" など)
            **kwargs: 検出器固有の初期化パラメータ
        """
        # 現在アクティブな場合は停止
        self.is_active = False
        
        # 検出器を切り替え
        self.initialize_detector(detector_type, **kwargs)