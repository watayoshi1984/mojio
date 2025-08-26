# -*- coding: utf-8 -*-
"""
Voice Activity Detection Manager for Mojio
Mojio 音声区間検出管理クラス

音声区間検出機能の統合管理クラス
"""

import numpy as np
from typing import List, Tuple, Optional
from .vad_interface import VoiceActivityDetectionInterface
from .silero_vad import SileroVoiceActivityDetection


class VoiceActivityDetectionManager:
    """
    音声区間検出機能の統合管理クラス
    
    さまざまなVAD実装を統一的に管理し、
    アプリケーション全体から簡単に利用できるようにする
    """
    
    def __init__(self):
        """音声区間検出管理クラスを初期化"""
        self.current_vad: Optional[VoiceActivityDetectionInterface] = None
        self.current_vad_type: Optional[str] = None
        self.is_active = False
        self.sample_rate = 16000
        
    def initialize_vad(self, vad_type: str = "silero", sample_rate: int = 16000) -> None:
        """
        音声区間検出エンジンを初期化する
        
        Args:
            vad_type: VADエンジンの種類 ("silero" など)
            sample_rate: サンプリングレート (Hz)
        """
        self.sample_rate = sample_rate
        
        if vad_type == "silero":
            self.current_vad = SileroVoiceActivityDetection()
            self.current_vad.initialize(sample_rate)
            self.current_vad_type = vad_type
        else:
            raise ValueError(f"サポートされていないVADエンジンタイプ: {vad_type}")
            
        self.is_active = True
        
    def is_speech(self, audio_data: np.ndarray) -> bool:
        """
        音声データに音声が含まれているか判定する
        
        Args:
            audio_data: 音声データ (numpy配列)
            
        Returns:
            bool: 音声が含まれている場合はTrue、そうでない場合はFalse
        """
        if not self.is_active or self.current_vad is None:
            raise RuntimeError("音声区間検出エンジンが初期化されていません。initialize_vad()を先に呼び出してください。")
            
        return self.current_vad.is_speech(audio_data)
    
    def detect_speech_segments(self, audio_data: np.ndarray) -> List[Tuple[float, float]]:
        """
        音声データから音声区間を検出する
        
        Args:
            audio_data: 音声データ (numpy配列)
            
        Returns:
            list: 音声区間のリスト [(start_time, end_time), ...]
        """
        if not self.is_active or self.current_vad is None:
            raise RuntimeError("音声区間検出エンジンが初期化されていません。initialize_vad()を先に呼び出してください。")
            
        return self.current_vad.detect_speech_segments(audio_data)
    
    def switch_vad(self, vad_type: str, sample_rate: int = 16000) -> None:
        """
        VADエンジンを切り替える
        
        Args:
            vad_type: VADエンジンの種類 ("silero" など)
            sample_rate: サンプリングレート (Hz)
        """
        self.initialize_vad(vad_type, sample_rate)
        
    def reset(self) -> None:
        """
        VADの内部状態をリセットする
        """
        if self.current_vad is not None:
            self.current_vad.reset()