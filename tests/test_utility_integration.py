# -*- coding: utf-8 -*-
"""
Integration tests for utility features
ユーティリティ機能の統合テスト
"""

import unittest
import os
import tempfile
import shutil
from src.mojio.data.history_manager import HistoryManager
from src.mojio.data.profile_manager import ProfileManager
from src.mojio.data.export_manager import ExportManager


class TestUtilityIntegration(unittest.TestCase):
    """ユーティリティ機能統合テストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        # 一時データベースファイルを作成
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # 履歴管理を初期化
        self.history_manager = HistoryManager()
        self.history_manager.initialize(self.db_path)
        
        # プロファイル管理を初期化
        self.profile_manager = ProfileManager()
        self.profile_manager.initialize(self.db_path)
        
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
            
        if hasattr(self, 'profile_manager') and self.profile_manager:
            self.profile_manager.db_manager.disconnect()
        
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
            shutil.rmtree(self.temp_dir)
                    
    def test_history_profile_integration(self):
        """履歴とプロファイルの統合テスト"""
        # プロファイルを作成
        settings = {"input_type": "microphone", "vad_enabled": True, "history_enabled": True}
        result = self.profile_manager.create_profile("テストプロファイル", settings)
        self.assertTrue(result)
        
        # 履歴にエントリを追加
        result = self.history_manager.add_entry("テスト文字起こし結果", "2023-01-01T00:00:00", "話者1")
        self.assertTrue(result)
        
        # 履歴エントリを取得
        entries = self.history_manager.list_entries()
        self.assertEqual(len(entries), 1)
        
        # プロファイルを取得
        profile = self.profile_manager.get_profile_by_name("テストプロファイル")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["settings"]["history_enabled"], True)
        
    def test_export_history_integration(self):
        """エクスポートと履歴の統合テスト"""
        # 履歴にテストデータを追加
        self.history_manager.add_entry("テストテキスト1", "2023-01-01T00:00:00", "話者1")
        self.history_manager.add_entry("テストテキスト2", "2023-01-01T00:01:00", "話者2")
        
        # テキストファイルにエクスポート
        output_file = os.path.join(self.temp_dir, "integration_output.txt")
        result = self.export_manager.export_history_to_text(output_file)
        self.assertTrue(result)
        
        # ファイルが作成されたことを確認
        self.assertTrue(os.path.exists(output_file))
        
        # ファイルの内容を確認
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("[2023-01-01T00:00:00] 話者1: テストテキスト1", content)
            self.assertIn("[2023-01-01T00:01:00] 話者2: テストテキスト2", content)
            
    def test_full_utility_workflow(self):
        """ユーティリティ機能全体のワークフロー統合テスト"""
        # 1. プロファイルを作成
        profile_settings = {
            "input_type": "microphone", 
            "vad_enabled": True, 
            "history_enabled": True,
            "export_format": "text"
        }
        result = self.profile_manager.create_profile("統合テストプロファイル", profile_settings)
        self.assertTrue(result)
        
        # 2. 音声認識結果を履歴に保存
        transcription_results = [
            {"text": "これは最初のテスト結果です", "timestamp": "2023-01-01T00:00:00", "speaker": "話者A"},
            {"text": "これは2番目のテスト結果です", "timestamp": "2023-01-01T00:01:00", "speaker": "話者B"},
            {"text": "これは最後のテスト結果です", "timestamp": "2023-01-01T00:02:00", "speaker": "話者A"}
        ]
        
        for result in transcription_results:
            self.history_manager.add_entry(
                result["text"], 
                result["timestamp"], 
                result["speaker"]
            )
        
        # 3. 履歴をエクスポート
        export_file = os.path.join(self.temp_dir, "full_workflow_output.txt")
        export_result = self.export_manager.export_history_to_text(export_file)
        self.assertTrue(export_result)
        
        # 4. エクスポートされたファイルの内容を検証
        self.assertTrue(os.path.exists(export_file))
        with open(export_file, "r", encoding="utf-8") as f:
            content = f.read()
            for result in transcription_results:
                expected_line = f"[{result['timestamp']}] {result['speaker']}: {result['text']}"
                self.assertIn(expected_line, content)
                
        # 5. プロファイル設定を検証
        profile = self.profile_manager.get_profile_by_name("統合テストプロファイル")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["settings"]["export_format"], "text")
        self.assertEqual(profile["settings"]["history_enabled"], True)


if __name__ == "__main__":
    unittest.main()