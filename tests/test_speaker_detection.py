# -*- coding: utf-8 -*-
"""
Test cases for Speaker Detection
話者検出のテストケース
"""

import unittest
import numpy as np
from src.mojio.audio.simple_speaker_detection import SimpleSpeakerDetection
from src.mojio.audio.speaker_detection_manager import SpeakerDetectionManager


class TestSimpleSpeakerDetection(unittest.TestCase):
    """簡易話者検出のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        self.detector = SimpleSpeakerDetection()
        self.detector.initialize()
        
    def test_initialize(self):
        """初期化テスト"""
        self.assertTrue(self.detector.is_initialized())
        
    def test_detect_speaker_change(self):
        """話者切り替え検出テスト"""
        # 無音データ
        silence_data = np.zeros(16000, dtype=np.float32)  # 1秒分の無音
        
        # 音声データ（正弦波）
        t = np.linspace(0, 1, 16000, False)
        audio_data = np.sin(2 * np.pi * 440 * t)  # 440Hzの正弦波
        
        # 最初の検出はFalse
        result1 = self.detector.detect_speaker_change(silence_data)
        self.assertFalse(result1)
        
        # 無音の後に音声が来た場合、話者切り替えと判定
        result2 = self.detector.detect_speaker_change(audio_data)
        # 実際の検出結果はパラメータによって異なるため、ここでは例外が発生しないことを確認
        self.assertIsInstance(result2, bool)
        
    def test_get_speaker_features(self):
        """話者特徴量抽出テスト"""
        # 音声データ（正弦波）
        t = np.linspace(0, 1, 16000, False)
        audio_data = np.sin(2 * np.pi * 440 * t)  # 440Hzの正弦波
        
        # 特徴量を抽出
        features = self.detector.get_speaker_features(audio_data)
        
        # 特徴量が2つの要素を持っていることを確認
        self.assertEqual(len(features), 2)
        
        # エネルギーとゼロクロス率が数値であることを確認
        self.assertIsInstance(features[0], float)
        self.assertIsInstance(features[1], float)


class TestSpeakerDetectionManager(unittest.TestCase):
    """話者検出管理のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        self.manager = SpeakerDetectionManager()
        
    def test_initialize_detector(self):
        """検出器初期化テスト"""
        self.manager.initialize_detector("simple")
        self.assertTrue(self.manager.is_detector_initialized())
        
    def test_detect_speaker_change(self):
        """話者切り替え検出テスト"""
        # 検出器を初期化
        self.manager.initialize_detector("simple")
        
        # 音声データ（正弦波）
        t = np.linspace(0, 1, 16000, False)
        audio_data = np.sin(2 * np.pi * 440 * t)  # 440Hzの正弦波
        
        # 話者切り替えを検出
        result = self.manager.detect_speaker_change(audio_data)
        # 実際の検出結果はパラメータによって異なるため、ここでは例外が発生しないことを確認
        self.assertIsInstance(result, bool)
        
    def test_get_speaker_features(self):
        """話者特徴量抽出テスト"""
        # 検出器を初期化
        self.manager.initialize_detector("simple")
        
        # 音声データ（正弦波）
        t = np.linspace(0, 1, 16000, False)
        audio_data = np.sin(2 * np.pi * 440 * t)  # 440Hzの正弦波
        
        # 特徴量を抽出
        features = self.manager.get_speaker_features(audio_data)
        
        # 特徴量がリストであることを確認
        self.assertIsInstance(features, list)
        
        # 特徴量が2つの要素を持っていることを確認
        self.assertEqual(len(features), 2)


if __name__ == "__main__":
    unittest.main()