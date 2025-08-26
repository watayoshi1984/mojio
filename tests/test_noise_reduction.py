# -*- coding: utf-8 -*-
"""
Test cases for Noise Reduction
ノイズ除去機能のテストケース
"""

import unittest
import numpy as np
from src.mojio.audio.noise_reduction import SpectralGatingNoiseReduction
from src.mojio.audio.deep_learning_noise_reduction import DeepLearningNoiseReduction
from src.mojio.audio.noise_reduction_manager import NoiseReductionManager


class TestSpectralGatingNoiseReduction(unittest.TestCase):
    """スペクトルゲート方式ノイズ除去のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        self.noise_reducer = SpectralGatingNoiseReduction()
        self.sample_rate = 16000
        
    def test_initialize(self):
        """初期化テスト"""
        # 初期化
        self.noise_reducer.initialize(self.sample_rate)
        
        # 初期化フラグがTrueになっていることを確認
        self.assertTrue(self.noise_reducer.is_initialized)
        
        # サンプリングレートが正しく設定されていることを確認
        self.assertEqual(self.noise_reducer.sample_rate, self.sample_rate)
        
    def test_reduce_noise(self):
        """ノイズ除去テスト"""
        # 初期化
        self.noise_reducer.initialize(self.sample_rate)
        
        # テスト用の音声データを作成（単純な正弦波にノイズを加える）
        duration = 1.0  # 1秒
        freq = 440.0    # 440Hzの音
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        audio_data = np.sin(2 * np.pi * freq * t) + 0.1 * np.random.randn(len(t))
        
        # ノイズ除去を実行
        reduced_audio = self.noise_reducer.reduce_noise(audio_data)
        
        # 出力がnumpy配列であることを確認
        self.assertIsInstance(reduced_audio, np.ndarray)
        
        # 出力の長さが入力と一致することを確認
        self.assertEqual(len(reduced_audio), len(audio_data))
        
    def test_reset(self):
        """リセットテスト"""
        # 初期化
        self.noise_reducer.initialize(self.sample_rate)
        
        # リセットを実行（エラーが発生しなければOK）
        try:
            self.noise_reducer.reset()
            reset_success = True
        except Exception:
            reset_success = False
            
        self.assertTrue(reset_success)
        
    def test_reduce_noise_without_initialization(self):
        """初期化せずにノイズ除去を実行した場合のテスト"""
        # テスト用の音声データを作成
        audio_data = np.random.randn(1000)
        
        # 初期化せずにノイズ除去を実行するとRuntimeErrorが発生することを確認
        with self.assertRaises(RuntimeError):
            self.noise_reducer.reduce_noise(audio_data)


class TestDeepLearningNoiseReduction(unittest.TestCase):
    """深層学習ベースノイズ除去のテストクラス（未実装）"""
    
    def setUp(self):
        """テスト前処理"""
        self.noise_reducer = DeepLearningNoiseReduction()
        self.sample_rate = 16000
        
    def test_initialize(self):
        """初期化テスト"""
        # 初期化
        self.noise_reducer.initialize(self.sample_rate)
        
        # 初期化フラグがTrueになっていることを確認
        self.assertTrue(self.noise_reducer.is_initialized)
        
        # サンプリングレートが正しく設定されていることを確認
        self.assertEqual(self.noise_reducer.sample_rate, self.sample_rate)
        
    def test_reduce_noise(self):
        """ノイズ除去テスト（ダミー）"""
        # 初期化
        self.noise_reducer.initialize(self.sample_rate)
        
        # テスト用の音声データを作成
        audio_data = np.random.randn(1000)
        
        # ノイズ除去を実行（ダミーの処理を返す）
        reduced_audio = self.noise_reducer.reduce_noise(audio_data)
        
        # 出力がnumpy配列であることを確認
        self.assertIsInstance(reduced_audio, np.ndarray)
        
        # 出力の長さが入力と一致することを確認
        self.assertEqual(len(reduced_audio), len(audio_data))
        
    def test_reset(self):
        """リセットテスト"""
        # 初期化
        self.noise_reducer.initialize(self.sample_rate)
        
        # リセットを実行（エラーが発生しなければOK）
        try:
            self.noise_reducer.reset()
            reset_success = True
        except Exception:
            reset_success = False
            
        self.assertTrue(reset_success)
        
    def test_reduce_noise_without_initialization(self):
        """初期化せずにノイズ除去を実行した場合のテスト"""
        # テスト用の音声データを作成
        audio_data = np.random.randn(1000)
        
        # 初期化せずにノイズ除去を実行するとRuntimeErrorが発生することを確認
        with self.assertRaises(RuntimeError):
            self.noise_reducer.reduce_noise(audio_data)


class TestNoiseReductionManager(unittest.TestCase):
    """ノイズ除去管理のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        self.noise_reduction_manager = NoiseReductionManager()
        self.sample_rate = 16000
        
    def test_initialize(self):
        """初期化テスト"""
        # 初期化
        self.noise_reduction_manager.initialize("spectral_gating", self.sample_rate)
        
        # 初期化フラグがTrueになっていることを確認
        self.assertTrue(self.noise_reduction_manager.is_initialized)
        
        # アルゴリズムが正しく設定されていることを確認
        self.assertEqual(self.noise_reduction_manager.current_algorithm, "spectral_gating")
        
    def test_initialize_deep_learning(self):
        """深層学習ベースの初期化テスト"""
        # 初期化
        self.noise_reduction_manager.initialize("deep_learning", self.sample_rate)
        
        # 初期化フラグがTrueになっていることを確認
        self.assertTrue(self.noise_reduction_manager.is_initialized)
        
        # アルゴリズムが正しく設定されていることを確認
        self.assertEqual(self.noise_reduction_manager.current_algorithm, "deep_learning")
        
    def test_initialize_with_invalid_algorithm(self):
        """無効なアルゴリズムで初期化した場合のテスト"""
        # 無効なアルゴリズムで初期化するとValueErrorが発生することを確認
        with self.assertRaises(ValueError):
            self.noise_reduction_manager.initialize("invalid_algorithm", self.sample_rate)
            
    def test_reduce_noise(self):
        """ノイズ除去テスト"""
        # 初期化
        self.noise_reduction_manager.initialize("spectral_gating", self.sample_rate)
        
        # テスト用の音声データを作成（単純な正弦波にノイズを加える）
        duration = 1.0  # 1秒
        freq = 440.0    # 440Hzの音
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        audio_data = np.sin(2 * np.pi * freq * t) + 0.1 * np.random.randn(len(t))
        
        # ノイズ除去を実行
        reduced_audio = self.noise_reduction_manager.reduce_noise(audio_data)
        
        # 出力がnumpy配列であることを確認
        self.assertIsInstance(reduced_audio, np.ndarray)
        
        # 出力の長さが入力と一致することを確認
        self.assertEqual(len(reduced_audio), len(audio_data))
        
    def test_reduce_noise_without_initialization(self):
        """初期化せずにノイズ除去を実行した場合のテスト"""
        # テスト用の音声データを作成
        audio_data = np.random.randn(1000)
        
        # 初期化せずにノイズ除去を実行するとRuntimeErrorが発生することを確認
        with self.assertRaises(RuntimeError):
            self.noise_reduction_manager.reduce_noise(audio_data)
            
    def test_reset(self):
        """リセットテスト"""
        # 初期化
        self.noise_reduction_manager.initialize("spectral_gating", self.sample_rate)
        
        # リセットを実行（エラーが発生しなければOK）
        try:
            self.noise_reduction_manager.reset()
            reset_success = True
        except Exception:
            reset_success = False
            
        self.assertTrue(reset_success)


if __name__ == "__main__":
    unittest.main()