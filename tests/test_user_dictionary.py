# -*- coding: utf-8 -*-
"""
Test cases for User Dictionary
ユーザー辞書のテストケース
"""

import unittest
import os
import tempfile
from src.mojio.data.user_dictionary import UserDictionary


class TestUserDictionary(unittest.TestCase):
    """ユーザー辞書のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        # 一時データベースファイルを作成
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # ユーザー辞書を初期化
        self.user_dict = UserDictionary()
        self.user_dict.initialize(self.db_path)
        
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
            
    def test_add_entry(self):
        """エントリ追加テスト"""
        # エントリを追加
        result = self.user_dict.add_entry("テスト", "てすと", "一般")
        self.assertTrue(result)
        
        # エントリが追加されたことを確認
        entry = self.user_dict.search_entry("テスト")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["word"], "テスト")
        self.assertEqual(entry["reading"], "てすと")
        self.assertEqual(entry["category"], "一般")
        
    def test_update_entry(self):
        """エントリ更新テスト"""
        # エントリを追加
        self.user_dict.add_entry("テスト", "てすと", "一般")
        
        # エントリを更新
        result = self.user_dict.update_entry("テスト", reading="テストです")
        self.assertTrue(result)
        
        # エントリが更新されたことを確認
        entry = self.user_dict.search_entry("テスト")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["word"], "テスト")
        self.assertEqual(entry["reading"], "テストです")
        self.assertEqual(entry["category"], "一般")
        
    def test_delete_entry(self):
        """エントリ削除テスト"""
        # エントリを追加
        self.user_dict.add_entry("テスト", "てすと", "一般")
        
        # エントリを削除
        result = self.user_dict.delete_entry("テスト")
        self.assertTrue(result)
        
        # エントリが削除されたことを確認
        entry = self.user_dict.search_entry("テスト")
        self.assertIsNone(entry)
        
    def test_search_entry(self):
        """エントリ検索テスト"""
        # エントリを追加
        self.user_dict.add_entry("テスト", "てすと", "一般")
        
        # エントリを検索
        entry = self.user_dict.search_entry("テスト")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["word"], "テスト")
        self.assertEqual(entry["reading"], "てすと")
        self.assertEqual(entry["category"], "一般")
        
        # 存在しないエントリを検索
        entry = self.user_dict.search_entry("存在しない")
        self.assertIsNone(entry)
        
    def test_list_entries(self):
        """エントリ一覧取得テスト"""
        # 複数のエントリを追加
        self.user_dict.add_entry("テスト1", "てすと1", "一般")
        self.user_dict.add_entry("テスト2", "てすと2", "専門")
        self.user_dict.add_entry("テスト3", "てすと3", "一般")
        
        # すべてのエントリを取得
        entries = self.user_dict.list_entries()
        self.assertEqual(len(entries), 3)
        
        # カテゴリでフィルタリング
        entries = self.user_dict.list_entries("一般")
        self.assertEqual(len(entries), 2)
        for entry in entries:
            self.assertEqual(entry["category"], "一般")
            
    def test_load_dictionary(self):
        """辞書ロードテスト"""
        # 一時JSONファイルを作成
        temp_json = tempfile.NamedTemporaryFile(delete=False, suffix='.json', mode='w', encoding='utf-8')
        temp_json.write('[{"word": "テスト", "reading": "てすと", "category": "一般"}]')
        temp_json.close()
        
        try:
            # 辞書をロード
            result = self.user_dict.load_dictionary(temp_json.name)
            self.assertTrue(result)
            
            # エントリが追加されたことを確認
            entry = self.user_dict.search_entry("テスト")
            self.assertIsNotNone(entry)
            self.assertEqual(entry["word"], "テスト")
            self.assertEqual(entry["reading"], "てすと")
            self.assertEqual(entry["category"], "一般")
        finally:
            # 一時JSONファイルを削除
            if os.path.exists(temp_json.name):
                os.unlink(temp_json.name)
                
    def test_save_dictionary(self):
        """辞書保存テスト"""
        # エントリを追加
        self.user_dict.add_entry("テスト", "てすと", "一般")
        
        # 一時JSONファイルを作成
        temp_json = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_json.close()
        
        try:
            # 辞書を保存
            result = self.user_dict.save_dictionary(temp_json.name)
            self.assertTrue(result)
            
            # ファイルが作成されたことを確認
            self.assertTrue(os.path.exists(temp_json.name))
            
            # ファイルの内容を確認
            with open(temp_json.name, 'r', encoding='utf-8') as f:
                import json
                data = json.load(f)
                self.assertEqual(len(data), 1)
                self.assertEqual(data[0]["word"], "テスト")
                self.assertEqual(data[0]["reading"], "てすと")
                self.assertEqual(data[0]["category"], "一般")
        finally:
            # 一時JSONファイルを削除
            if os.path.exists(temp_json.name):
                os.unlink(temp_json.name)


if __name__ == "__main__":
    unittest.main()