# -*- coding: utf-8 -*-
"""
Test cases for History
履歴管理のテストケース
"""

import unittest
import os
import tempfile
from src.mojio.data.history_manager import HistoryManager


class TestHistoryManager(unittest.TestCase):
    """履歴管理のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        # 一時データベースファイルを作成
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # 履歴管理を初期化
        self.history_manager = HistoryManager()
        self.history_manager.initialize(self.db_path)
        
    def tearDown(self):
        """テスト後処理"""
        # データベース接続を閉じる
        if hasattr(self, 'history_manager') and self.history_manager:
            self.history_manager.db_manager.disconnect()
        
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
                    
    def test_add_entry(self):
        """エントリ追加テスト"""
        # エントリを追加
        result = self.history_manager.add_entry("テスト文字起こし結果", "2023-01-01T00:00:00", "話者1")
        self.assertTrue(result)
        
        # エントリが追加されたことを確認
        entries = self.history_manager.list_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["text"], "テスト文字起こし結果")
        self.assertEqual(entries[0]["timestamp"], "2023-01-01T00:00:00")
        self.assertEqual(entries[0]["speaker"], "話者1")
        
    def test_delete_entry(self):
        """エントリ削除テスト"""
        # エントリを追加
        self.history_manager.add_entry("テスト文字起こし結果", "2023-01-01T00:00:00", "話者1")
        
        # エントリを削除
        entries = self.history_manager.list_entries()
        entry_id = entries[0]["id"]
        result = self.history_manager.delete_entry(entry_id)
        self.assertTrue(result)
        
        # エントリが削除されたことを確認
        entries = self.history_manager.list_entries()
        self.assertEqual(len(entries), 0)
        
    def test_search_entries(self):
        """エントリ検索テスト"""
        # 複数のエントリを追加
        self.history_manager.add_entry("これはテストです", "2023-01-01T00:00:00", "話者1")
        self.history_manager.add_entry("別のテストエントリ", "2023-01-01T00:01:00", "話者2")
        self.history_manager.add_entry("テスト文字起こし結果", "2023-01-01T00:02:00", "話者1")
        
        # キーワードで検索
        results = self.history_manager.search_entries("テスト")
        self.assertEqual(len(results), 3)
        
        # 特定のキーワードで検索
        results = self.history_manager.search_entries("文字起こし")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "テスト文字起こし結果")
        
    def test_list_entries(self):
        """エントリ一覧取得テスト"""
        # 複数のエントリを追加
        self.history_manager.add_entry("エントリ1", "2023-01-01T00:00:00", "話者1")
        self.history_manager.add_entry("エントリ2", "2023-01-01T00:01:00", "話者2")
        self.history_manager.add_entry("エントリ3", "2023-01-01T00:02:00", "話者1")
        
        # すべてのエントリを取得
        entries = self.history_manager.list_entries()
        self.assertEqual(len(entries), 3)
        
        # 制限付きでエントリを取得
        entries = self.history_manager.list_entries(limit=2)
        self.assertEqual(len(entries), 2)
        
    def test_get_entry(self):
        """エントリ取得テスト"""
        # エントリを追加
        self.history_manager.add_entry("テスト文字起こし結果", "2023-01-01T00:00:00", "話者1")
        
        # エントリを取得
        entries = self.history_manager.list_entries()
        entry_id = entries[0]["id"]
        entry = self.history_manager.get_entry(entry_id)
        self.assertIsNotNone(entry)
        self.assertEqual(entry["text"], "テスト文字起こし結果")
        self.assertEqual(entry["timestamp"], "2023-01-01T00:00:00")
        self.assertEqual(entry["speaker"], "話者1")
        
        # 存在しないエントリを取得
        entry = self.history_manager.get_entry(999)
        self.assertIsNone(entry)


if __name__ == "__main__":
    unittest.main()