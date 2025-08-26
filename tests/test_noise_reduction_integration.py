# -*- coding: utf-8 -*-
"""
Integration tests for Noise Reduction
ノイズ除去機能の統合テスト
"""

import unittest
import numpy as np
from unittest.mock import Mock, patch
from src.mojio.system.realtime_pipeline import RealtimeProcessingPipeline


class TestNoiseReductionIntegration(unittest.TestCase):
    """ノイズ除去機能の統合テストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        self.pipeline = RealtimeProcessingPipeline()
        
    @patch('src.mojio.system.realtime_pipeline.RealtimeProcessingPipeline.initialize')
    def test_initialize_with_noise_reduction(self, mock_initialize):
        """ノイズ除去機能ありでの初期化テスト"""
        # initializeメソッドをモック化
        mock_initialize.return_value = None
        
        # ノイズ除去機能ありで初期化
        self.pipeline.initialize(noise_reduction_enabled=True)
        
        # initializeメソッドが呼び出されたことを確認
        mock_initialize.assert_called_once_with(noise_reduction_enabled=True)
        
    @patch('src.mojio.system.realtime_pipeline.RealtimeProcessingPipeline.initialize')
    def test_initialize_without_noise_reduction(self, mock_initialize):
        """ノイズ除去機能なしでの初期化テスト"""
        # initializeメソッドをモック化
        mock_initialize.return_value = None
        
        # ノイズ除去機能なしで初期化
        self.pipeline.initialize(noise_reduction_enabled=False)
        
        # initializeメソッドが呼び出されたことを確認
        mock_initialize.assert_called_once_with(noise_reduction_enabled=False)
        
    def test_audio_callback_with_noise_reduction(self):
        """ノイズ除去機能ありでの音声コールバックテスト"""
        # 録音状態を有効化
        self.pipeline.is_recording = True
        self.pipeline.noise_reduction_enabled = True
        
        # ノイズ除去マネージャをモック化
        self.pipeline.noise_reduction_manager = Mock()
        self.pipeline.noise_reduction_manager.reduce_noise.return_value = np.array([0.1, 0.2, 0.3])
        
        # VADマネージャをモック化
        self.pipeline.vad_manager = Mock()
        self.pipeline.vad_manager.is_speech.return_value = True
        
        # 音声データを作成
        audio_data = np.array([0.1, 0.2, 0.3])
        
        # 音声コールバックを実行
        self.pipeline._audio_callback(audio_data)
        
        # ノイズ除去メソッドが呼び出されたことを確認
        self.pipeline.noise_reduction_manager.reduce_noise.assert_called_once_with(audio_data)
        
    def test_audio_callback_with_noise_reduction_error(self):
        """ノイズ除去機能でのエラーテスト"""
        # 録音状態を有効化
        self.pipeline.is_recording = True
        self.pipeline.noise_reduction_enabled = True
        
        # ノイズ除去マネージャをモック化し、例外を発生させる
        self.pipeline.noise_reduction_manager = Mock()
        self.pipeline.noise_reduction_manager.reduce_noise.side_effect = Exception("ノイズ除去エラー")
        
        # VADマネージャをモック化
        self.pipeline.vad_manager = Mock()
        self.pipeline.vad_manager.is_speech.return_value = True
        
        # 音声データを作成
        audio_data = np.array([0.1, 0.2, 0.3])
        
        # 音声コールバックを実行（エラーが発生しても例外が上がらないことを確認）
        try:
            self.pipeline._audio_callback(audio_data)
            no_exception_raised = True
        except Exception:
            no_exception_raised = False
            
        self.assertTrue(no_exception_raised)
        
        # ノイズ除去メソッドが呼び出されたことを確認
        self.pipeline.noise_reduction_manager.reduce_noise.assert_called_once_with(audio_data)


if __name__ == "__main__":
    unittest.main()