# -*- coding: utf-8 -*-
"""
Test cases for Export
エクスポート機能のテストケース
"""

import unittest
import os
import tempfile
from src.mojio.data.export_manager import ExportManager
from src.mojio.data.history_manager import HistoryManager


class TestExportManager(unittest.TestCase):
    """エクスポート管理のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        # 一時データベースファイルを作成
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # 履歴管理を初期化
        self.history_manager = HistoryManager()
        self.history_manager.initialize(self.db_path)
        
        # エクスポート管理を初期化
        self.export_manager = ExportManager()
        self.export_manager.initialize(self.history_manager)
        
        # 一時出力ディレクトリを作成
        self.temp_dir = tempfile.mkdtemp()
        
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
        
        # 一時出力ディレクトリを削除
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
                    
    def test_export_to_text(self):
        """テキストファイルへのエクスポートテスト"""
        # テストデータを作成
        test_data = [
            {"text": "テストテキスト1", "timestamp": "2023-01-01T00:00:00", "speaker": "話者1"},
            {"text": "テストテキスト2", "timestamp": "2023-01-01T00:01:00", "speaker": "話者2"}
        ]
        
        # テキストファイルにエクスポート
        output_file = os.path.join(self.temp_dir, "test_output.txt")
        result = self.export_manager.export_to_text(test_data, output_file)
        self.assertTrue(result)
        
        # ファイルが作成されたことを確認
        self.assertTrue(os.path.exists(output_file))
        
        # ファイルの内容を確認
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("[2023-01-01T00:00:00] 話者1: テストテキスト1", content)
            self.assertIn("[2023-01-01T00:01:00] 話者2: テストテキスト2", content)
        
    def test_export_to_srt(self):
        """SRTファイルへのエクスポートテスト"""
        # テストデータを作成
        test_data = [
            {"text": "テストテキスト1"},
            {"text": "テストテキスト2"}
        ]
        
        # SRTファイルにエクスポート
        output_file = os.path.join(self.temp_dir, "test_output.srt")
        result = self.export_manager.export_to_srt(test_data, output_file)
        self.assertTrue(result)
        
        # ファイルが作成されたことを確認
        self.assertTrue(os.path.exists(output_file))
        
        # ファイルの内容を確認
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("1", content)
            self.assertIn("00:00:05,000 --> 00:00:09,000", content)
            self.assertIn("テストテキスト1", content)
            self.assertIn("2", content)
            self.assertIn("00:00:10,000 --> 00:00:14,000", content)
            self.assertIn("テストテキスト2", content)
        
    def test_export_history_to_text(self):
        """履歴のテキストファイルへのエクスポートテスト"""
        # 履歴にテストデータを追加
        self.history_manager.add_entry("テストテキスト1", "2023-01-01T00:00:00", "話者1")
        self.history_manager.add_entry("テストテキスト2", "2023-01-01T00:01:00", "話者2")
        
        # テキストファイルにエクスポート
        output_file = os.path.join(self.temp_dir, "history_output.txt")
        result = self.export_manager.export_history_to_text(output_file)
        self.assertTrue(result)
        
        # ファイルが作成されたことを確認
        self.assertTrue(os.path.exists(output_file))
        
        # ファイルの内容を確認
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("[2023-01-01T00:00:00] 話者1: テストテキスト1", content)
            self.assertIn("[2023-01-01T00:01:00] 話者2: テストテキスト2", content)
        
    def test_export_history_to_srt(self):
        """履歴のSRTファイルへのエクスポートテスト"""
        # 履歴にテストデータを追加
        self.history_manager.add_entry("テストテキスト1")
        self.history_manager.add_entry("テストテキスト2")
        
        # SRTファイルにエクスポート
        output_file = os.path.join(self.temp_dir, "history_output.srt")
        result = self.export_manager.export_history_to_srt(output_file)
        self.assertTrue(result)
        
        # ファイルが作成されたことを確認
        self.assertTrue(os.path.exists(output_file))
        
        # ファイルの内容を確認
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("1", content)
            self.assertIn("テストテキスト1", content)
            self.assertIn("2", content)
            self.assertIn("テストテキスト2", content)


if __name__ == "__main__":
    unittest.main()