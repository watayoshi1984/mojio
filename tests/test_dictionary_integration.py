# -*- coding: utf-8 -*-
"""
Test cases for Dictionary Integration in Real-time Pipeline
リアルタイム処理パイプラインでの辞書統合テスト
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import numpy as np

from src.mojio.system.realtime_pipeline import RealtimeProcessingPipeline


class TestDictionaryIntegration(unittest.TestCase):
    """リアルタイム処理パイプラインでの辞書統合テストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        with patch('src.mojio.system.realtime_pipeline.AudioInputManager'), \
             patch('src.mojio.system.realtime_pipeline.VoiceActivityDetectionManager'), \
             patch('src.mojio.system.realtime_pipeline.SpeechRecognitionManager'), \
             patch('src.mojio.system.realtime_pipeline.TextInjectionManager'), \
             patch('src.mojio.system.realtime_pipeline.GlobalShortcutManager'):
            self.pipeline = RealtimeProcessingPipeline()
            
        # モックオブジェクトを設定
        self.pipeline.recognition_manager = Mock()
        self.pipeline.text_injection_manager = Mock()
        self.pipeline.dictionary_manager = Mock()
        self.pipeline.matching_manager = Mock()
        
        # パイプラインをアクティブ状態にする
        self.pipeline.is_active = True
        
    def test_toggle_recording_with_dictionary_matching(self):
        """録音切り替え時の辞書マッチングテスト"""
        # テストデータを設定
        self.pipeline.is_recording = True
        self.pipeline.audio_buffer = [np.zeros(1024, dtype=np.float32)]
        self.pipeline.recognition_manager.transcribe.return_value = "これはテストです"
        
        # 辞書データをモック
        self.pipeline.dictionary_manager.list_entries.return_value = [
            {"word": "テスト", "reading": "てすと"}
        ]
        
        # 辞書マッチングの結果をモック
        self.pipeline.matching_manager.apply_dictionary.return_value = "これはてすとです"
        
        # 録音停止（辞書マッチングが適用される）
        self.pipeline.is_recording = False
        self.pipeline._toggle_recording()
        
        # メソッド呼び出しが正しいことを検証
        self.pipeline.recognition_manager.transcribe.assert_called_once()
        self.pipeline.dictionary_manager.list_entries.assert_called_once()
        self.pipeline.matching_manager.apply_dictionary.assert_called_once_with(
            "これはテストです", {"テスト": "てすと"}
        )
        self.pipeline.text_injection_manager.inject_text.assert_called_once_with(
            "これはてすとです", None
        )
        
    def test_audio_callback_with_dictionary_matching(self):
        """音声コールバックでの辞書マッチングテスト"""
        # VADを有効化
        self.pipeline.vad_enabled = True
        self.pipeline.vad_manager = Mock()
        self.pipeline.vad_manager.is_speech.return_value = False
        
        # テストデータを設定
        self.pipeline.is_recording = True
        self.pipeline.audio_buffer = [np.zeros(1024, dtype=np.float32)]
        self.pipeline.recognition_manager.transcribe.return_value = "これはテストです"
        
        # 辞書データをモック
        self.pipeline.dictionary_manager.list_entries.return_value = [
            {"word": "テスト", "reading": "てすと"}
        ]
        
        # 辞書マッチングの結果をモック
        self.pipeline.matching_manager.apply_dictionary.return_value = "これはてすとです"
        
        # 音声コールバックを実行（辞書マッチングが適用される）
        audio_data = np.zeros(512, dtype=np.float32)
        self.pipeline._audio_callback(audio_data)
        
        # メソッド呼び出しが正しいことを検証
        self.pipeline.recognition_manager.transcribe.assert_called_once()
        self.pipeline.dictionary_manager.list_entries.assert_called_once()
        self.pipeline.matching_manager.apply_dictionary.assert_called_once_with(
            "これはテストです", {"テスト": "てすと"}
        )
        self.pipeline.text_injection_manager.inject_text.assert_called_once_with(
            "これはてすとです", None
        )


if __name__ == "__main__":
    unittest.main()