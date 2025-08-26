# -*- coding: utf-8 -*-
"""
Test cases for Core Features
コア機能のテストケース
"""

import unittest
import numpy as np

# モジュールのインポートに失敗した場合の処理
try:
    from src.mojio.audio.audio_manager import AudioInputManager
    AUDIO_MANAGER_AVAILABLE = True
except ImportError:
    AUDIO_MANAGER_AVAILABLE = False
    AudioInputManager = None

try:
    from src.mojio.audio.recognition_manager import SpeechRecognitionManager
    RECOGNITION_MANAGER_AVAILABLE = True
except ImportError:
    RECOGNITION_MANAGER_AVAILABLE = False
    SpeechRecognitionManager = None

try:
    from src.mojio.system.text_injection_manager import TextInjectionManager
    TEXT_INJECTION_MANAGER_AVAILABLE = True
except ImportError:
    TEXT_INJECTION_MANAGER_AVAILABLE = False
    TextInjectionManager = None


class TestCoreFeatures(unittest.TestCase):
    """コア機能のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        # 音声入力管理を初期化
        if AUDIO_MANAGER_AVAILABLE:
            self.audio_manager = AudioInputManager()
        else:
            self.audio_manager = None
        
        # 音声認識管理を初期化
        if RECOGNITION_MANAGER_AVAILABLE:
            self.recognition_manager = SpeechRecognitionManager()
            try:
                self.recognition_manager.initialize_engine(engine_type="whisper", model_size="tiny")
            except Exception:
                # Whisperモデルの初期化に失敗した場合はNoneにする
                self.recognition_manager = None
        else:
            self.recognition_manager = None
        
        # テキスト挿入管理を初期化
        if TEXT_INJECTION_MANAGER_AVAILABLE:
            self.text_injection_manager = TextInjectionManager()
        else:
            self.text_injection_manager = None
        
    @unittest.skipUnless(AUDIO_MANAGER_AVAILABLE, "AudioInputManager not available")
    def test_audio_input_integration(self):
        """音声入力機能統合テスト"""
        # 音声入力管理が初期化されていることを確認
        self.assertIsNotNone(self.audio_manager)
        
        # マイクデバイス一覧を取得
        mic_devices = self.audio_manager.get_microphone_devices()
        # デバイス一覧がリストであることを確認
        self.assertIsInstance(mic_devices, list)
        
        # ループバックデバイス一覧を取得
        loopback_devices = self.audio_manager.get_loopback_devices()
        # デバイス一覧がリストであることを確認
        self.assertIsInstance(loopback_devices, list)
        
    @unittest.skipUnless(RECOGNITION_MANAGER_AVAILABLE, "SpeechRecognitionManager not available")
    def test_speech_recognition_integration(self):
        """音声認識機能統合テスト"""
        # 音声認識管理が初期化されていることを確認
        if self.recognition_manager is None:
            self.skipTest("音声認識エンジンの初期化に失敗しました")
            
        self.assertTrue(self.recognition_manager.is_engine_initialized())
        
        # ダミー音声データでテスト
        dummy_audio = np.zeros(16000, dtype=np.float32)  # 1秒分の無音データ
        
        # 音声認識を実行
        result = self.recognition_manager.transcribe(dummy_audio, language="ja")
        
        # 認識結果が文字列であることを確認
        self.assertIsInstance(result, str)
        
    @unittest.skipUnless(TEXT_INJECTION_MANAGER_AVAILABLE, "TextInjectionManager not available")
    def test_text_injection_integration(self):
        """テキスト挿入機能統合テスト"""
        # テキスト挿入管理が初期化されていることを確認
        self.assertIsNotNone(self.text_injection_manager)
        
        # アクティブウィンドウのタイトルを取得
        active_window = self.text_injection_manager.get_active_window_title()
        # ウィンドウタイトルが文字列であることを確認
        self.assertIsInstance(active_window, str)
        
    @unittest.skipUnless(AUDIO_MANAGER_AVAILABLE and RECOGNITION_MANAGER_AVAILABLE and TEXT_INJECTION_MANAGER_AVAILABLE, 
                        "All core modules not available")
    def test_all_features_integration(self):
        """全機能統合テスト"""
        # 音声入力管理が初期化されていることを確認
        self.assertIsNotNone(self.audio_manager)
        
        # 音声認識管理が初期化されていることを確認
        if self.recognition_manager is None:
            self.skipTest("音声認識エンジンの初期化に失敗しました")
        self.assertTrue(self.recognition_manager.is_engine_initialized())
        
        # テキスト挿入管理が初期化されていることを確認
        self.assertIsNotNone(self.text_injection_manager)
        
        # ダミー音声データでテスト
        dummy_audio = np.zeros(16000, dtype=np.float32)  # 1秒分の無音データ
        
        # 音声認識を実行
        recognized_text = self.recognition_manager.transcribe(dummy_audio, language="ja")
        
        # 認識結果が文字列であることを確認
        self.assertIsInstance(recognized_text, str)
        
        # アクティブウィンドウのタイトルを取得
        active_window = self.text_injection_manager.get_active_window_title()
        # ウィンドウタイトルが文字列であることを確認
        self.assertIsInstance(active_window, str)


if __name__ == "__main__":
    unittest.main()