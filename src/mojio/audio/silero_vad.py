# -*- coding: utf-8 -*-
"""
Silero VAD Implementation for Mojio
Mojio Silero 音声区間検出実装

Silero VADを使用した音声区間検出の具体実装
"""

import numpy as np
from typing import List, Tuple
import torch
from .vad_interface import VoiceActivityDetectionInterface

try:
    import silero_vad
except ImportError:
    silero_vad = None


class SileroVoiceActivityDetection(VoiceActivityDetectionInterface):
    """
    Silero VADを使用した音声区間検出実装
    
    Silero VADモデルを使用して音声の有無を判定し、
    発話区間を検出するためのクラス
    """
    
    def __init__(self):
        """Silero VADを初期化"""
        self.model = None
        self.sample_rate = 16000
        self.window_size_samples = 512  # Silero VADの推奨ウィンドウサイズ
        self.speech_prob_threshold = 0.5  # 音声判定の閾値
        self.is_initialized = False
        
    def initialize(self, sample_rate: int = 16000) -> None:
        """
        Silero VADモデルを初期化する
        
        Args:
            sample_rate: サンプリングレート (Hz)
        """
        if silero_vad is None:
            raise RuntimeError("silero_vad ライブラリがインストールされていません。")
            
        self.sample_rate = sample_rate
        self.window_size_samples = 512 if sample_rate == 16000 else 256
        
        # Silero VADモデルをロード
        self.model = silero_vad.load_silero_vad()
        self.is_initialized = True
        
    def is_speech(self, audio_data: np.ndarray) -> bool:
        """
        音声データに音声が含まれているか判定する
        
        Args:
            audio_data: 音声データ (numpy配列)
            
        Returns:
            bool: 音声が含まれている場合はTrue、そうでない場合はFalse
        """
        if not self.is_initialized:
            raise RuntimeError("VADモデルが初期化されていません。initialize()を先に呼び出してください。")
            
        if len(audio_data) != self.window_size_samples:
            raise ValueError(f"音声データの長さは {self.window_size_samples} サンプルである必要があります。")
            
        # PyTorchテンソルに変換
        audio_tensor = torch.from_numpy(audio_data).float()
        
        # 音声判定
        speech_prob = self.model(audio_tensor, self.sample_rate).item()
        return speech_prob > self.speech_prob_threshold
    
    def detect_speech_segments(self, audio_data: np.ndarray) -> List[Tuple[float, float]]:
        """
        音声データから音声区間を検出する
        
        Args:
            audio_data: 音声データ (numpy配列)
            
        Returns:
            list: 音声区間のリスト [(start_time, end_time), ...]
        """
        if not self.is_initialized:
            raise RuntimeError("VADモデルが初期化されていません。initialize()を先に呼び出してください。")
            
        segments = []
        current_segment_start = None
        current_time = 0.0
        time_per_sample = 1.0 / self.sample_rate
        
        # ウィンドウサイズでデータを分割して処理
        for i in range(0, len(audio_data), self.window_size_samples):
            window = audio_data[i:i + self.window_size_samples]
            
            # ウィンドウサイズに満たない場合はスキップ
            if len(window) != self.window_size_samples:
                continue
                
            # 音声判定
            if self.is_speech(window):
                # 音声区間の開始を記録
                if current_segment_start is None:
                    current_segment_start = current_time
            else:
                # 音声区間の終了を記録
                if current_segment_start is not None:
                    segments.append((current_segment_start, current_time))
                    current_segment_start = None
                    
            current_time += self.window_size_samples * time_per_sample
            
        # 最後の音声区間を追加
        if current_segment_start is not None:
            segments.append((current_segment_start, current_time))
            
        return segments
    
    def reset(self) -> None:
        """
        VADの内部状態をリセットする
        """
        if self.model is not None:
            # Silero VADモデルの内部状態をリセット
            self.model.reset_states()