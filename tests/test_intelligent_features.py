# -*- coding: utf-8 -*-
"""
Test cases for Intelligent Features
インテリジェント機能のテストケース
"""

import unittest
import tempfile
import os
import numpy as np
from src.mojio.data.user_dictionary import UserDictionary
from src.mojio.audio.speaker_detection_manager import SpeakerDetectionManager
from src.mojio.data.punctuation_manager import PunctuationManager


class TestIntelligentFeatures(unittest.TestCase):
    """インテリジェント機能のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        # 一時データベースファイルを作成
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # ユーザー辞書を初期化
        self.user_dict = UserDictionary()
        self.user_dict.initialize(self.db_path)
        
        # 話者検出を初期化
        self.speaker_detector = SpeakerDetectionManager()
        self.speaker_detector.initialize_detector("simple")
        
        # 句読点挿入を初期化
        self.punctuation = PunctuationManager()
        self.punctuation.initialize_punctuation("simple")
        
    def tearDown(self):
        """テスト後処理"""
        # データベース接続を閉じる
        if hasattr(self, 'user_dict') and self.user_dict:
            self.user_dict.db_manager.disconnect()
        
        # 一時データベースファイルを削除
        if hasattr(self, 'db_path') and os.path.exists(self.db_path):
            # ファイルが使用中の場合、数回リトライする
            import time
            for i in range(5):
                try:
                    os.unlink(self.db_path)
                    break
                except PermissionError:
                    if i == 4:  # 最後のリトライでも失敗した場合
                        raise
                    time.sleep(0.1)  # 0.1秒待機してからリトライ
                    
    def test_user_dictionary_integration(self):
        """ユーザー辞書機能統合テスト"""
        # ユーザー辞書にエントリを追加
        self.user_dict.add_entry("テスト", "てすと", "一般")
        
        # エントリが追加されたことを確認
        entry = self.user_dict.search_entry("テスト")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["word"], "テスト")
        self.assertEqual(entry["reading"], "てすと")
        self.assertEqual(entry["category"], "一般")
        
    def test_speaker_detection_integration(self):
        """話者識別機能統合テスト"""
        # 無音データ
        silence_data = np.zeros(16000, dtype=np.float32)  # 1秒分の無音
        
        # 音声データ（正弦波）
        t = np.linspace(0, 1, 16000, False)
        audio_data = np.sin(2 * np.pi * 440 * t)  # 440Hzの正弦波
        
        # 話者切り替えを検出
        result = self.speaker_detector.detect_speaker_change(silence_data)
        # 無音の後で音声が来た場合、話者切り替えと判定される可能性がある
        self.assertIsInstance(result, bool)
        
    def test_punctuation_integration(self):
        """句読点自動挿入機能統合テスト"""
        # 句読点が挿入されていないテキスト
        text = "今日は良い天気です明日も良い天気でしょう"
        result = self.punctuation.insert_punctuation(text)
        
        # 句点が挿入されることを確認
        self.assertIn("。", result)
        
        # 既に句読点が末尾にある場合は何もしない
        text_with_punctuation = "今日は良い天気です。"
        result = self.punctuation.insert_punctuation(text_with_punctuation)
        self.assertEqual(result, text_with_punctuation)
        
    def test_all_features_integration(self):
        """全機能統合テスト"""
        # ユーザー辞書にエントリを追加
        self.user_dict.add_entry("テスト", "てすと", "一般")
        
        # 音声データ（正弦波）
        t = np.linspace(0, 1, 16000, False)
        audio_data = np.sin(2 * np.pi * 440 * t)  # 440Hzの正弦波
        
        # 話者切り替えを検出
        speaker_changed = self.speaker_detector.detect_speaker_change(audio_data)
        self.assertIsInstance(speaker_changed, bool)
        
        # 句読点が挿入されていないテキスト
        text = "今日はテストです明日もテストでしょう"
        result = self.punctuation.insert_punctuation(text)
        
        # 句点が挿入されることを確認
        self.assertIn("。", result)
        
        # ユーザー辞書のエントリを検索
        entry = self.user_dict.search_entry("テスト")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["word"], "テスト")
        self.assertEqual(entry["reading"], "てすと")
        self.assertEqual(entry["category"], "一般")


if __name__ == "__main__":
    unittest.main()