# -*- coding: utf-8 -*-
"""
Error Handling Tests for MOJIO
MOJIO エラーハンドリングテスト

エラーハンドリング機能のユニットテスト
"""

import unittest
import os
import tempfile
import shutil
from pathlib import Path

from src.mojio.exceptions import (
    MojioBaseException,
    AudioInputError,
    SpeechRecognitionError,
    TextInjectionError,
    DatabaseError,
    ConfigurationError,
    ValidationError,
    InitializationError,
    FileNotFoundError,
    PermissionError,
    NetworkError,
    TimeoutError
)

from src.mojio.utils.logger import MojioLogger, get_logger, setup_logger


class TestCustomExceptions(unittest.TestCase):
    """カスタム例外クラスのテスト"""
    
    def test_mojio_base_exception(self):
        """基本例外クラスのテスト"""
        # エラーメッセージのみのケース
        exception = MojioBaseException("テストエラー")
        self.assertEqual(str(exception), "テストエラー")
        
        # エラーコード付きのケース
        exception = MojioBaseException("テストエラー", "TEST_ERROR")
        self.assertEqual(str(exception), "[TEST_ERROR] テストエラー")
        
    def test_audio_input_error(self):
        """音声入力エラーのテスト"""
        exception = AudioInputError("音声入力テストエラー")
        self.assertEqual(str(exception), "[AUDIO_INPUT_ERROR] 音声入力テストエラー")
        
    def test_speech_recognition_error(self):
        """音声認識エラーのテスト"""
        exception = SpeechRecognitionError("音声認識テストエラー")
        self.assertEqual(str(exception), "[SPEECH_RECOGNITION_ERROR] 音声認識テストエラー")
        
    def test_text_injection_error(self):
        """テキスト挿入エラーのテスト"""
        exception = TextInjectionError("テキスト挿入テストエラー")
        self.assertEqual(str(exception), "[TEXT_INJECTION_ERROR] テキスト挿入テストエラー")
        
    def test_database_error(self):
        """データベースエラーのテスト"""
        exception = DatabaseError("データベーステストエラー")
        self.assertEqual(str(exception), "[DATABASE_ERROR] データベーステストエラー")
        
    def test_configuration_error(self):
        """設定エラーのテスト"""
        exception = ConfigurationError("設定テストエラー")
        self.assertEqual(str(exception), "[CONFIGURATION_ERROR] 設定テストエラー")


class TestLogger(unittest.TestCase):
    """ロガークラスのテスト"""
    
    def setUp(self):
        """テスト前処理"""
        # 一時的なログディレクトリを作成
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_dir = Path(self.temp_dir.name) / "logs"
        
    def tearDown(self):
        """テスト後処理"""
        # ロガーをクリーンアップ
        from src.mojio.utils.logger import _logger
        if _logger:
            # ハンドラーをすべて削除
            for handler in _logger.logger.handlers[:]:
                handler.close()
                _logger.logger.removeHandler(handler)
        
        # グローバルロガーインスタンスをリセット
        from src.mojio.utils.logger import setup_logger
        setup_logger(str(self.log_dir))
        
        # 一時ディレクトリを削除
        self.temp_dir.cleanup()
        
    def test_logger_creation(self):
        """ロガー作成テスト"""
        logger = MojioLogger(str(self.log_dir))
        self.assertIsInstance(logger, MojioLogger)
        self.assertTrue(self.log_dir.exists())
        
    def test_logger_singleton(self):
        """ロガーのシングルトンパターンテスト"""
        logger1 = get_logger()
        logger2 = get_logger()
        self.assertIs(logger1, logger2)
        
    def test_logger_setup(self):
        """ロガーのセットアップテスト"""
        logger = setup_logger(str(self.log_dir))
        self.assertIsInstance(logger, MojioLogger)
        
    def test_log_methods(self):
        """ログメソッドのテスト"""
        logger = MojioLogger(str(self.log_dir))
        
        # 各ログレベルのテスト
        logger.debug("デバッグメッセージ")
        logger.info("情報メッセージ")
        logger.warning("警告メッセージ")
        logger.error("エラーメッセージ")
        logger.critical("致命的エラーメッセージ")
        logger.exception("例外メッセージ")


if __name__ == "__main__":
    unittest.main()