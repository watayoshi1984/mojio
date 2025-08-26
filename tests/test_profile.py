# -*- coding: utf-8 -*-
"""
Test cases for Profile
プロファイル管理のテストケース
"""

import unittest
import os
import tempfile
import json
from src.mojio.data.profile_manager import ProfileManager


class TestProfileManager(unittest.TestCase):
    """プロファイル管理のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        # 一時データベースファイルを作成
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # プロファイル管理を初期化
        self.profile_manager = ProfileManager()
        self.profile_manager.initialize(self.db_path)
        
    def tearDown(self):
        """テスト後処理"""
        # データベース接続を閉じる
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
                    
    def test_create_profile(self):
        """プロファイル作成テスト"""
        # プロファイルを作成
        settings = {"input_type": "microphone", "vad_enabled": True}
        result = self.profile_manager.create_profile("テストプロファイル", settings)
        self.assertTrue(result)
        
        # プロファイルが作成されたことを確認
        profiles = self.profile_manager.list_profiles()
        self.assertEqual(len(profiles), 4)  # デフォルト3個 + 新規1個
        self.assertEqual(profiles[3]["name"], "テストプロファイル")
        self.assertEqual(profiles[3]["settings"], settings)
        
    def test_update_profile(self):
        """プロファイル更新テスト"""
        # プロファイルを作成
        settings = {"input_type": "microphone", "vad_enabled": True}
        self.profile_manager.create_profile("テストプロファイル", settings)
        
        # プロファイルを更新
        profiles = self.profile_manager.list_profiles()
        profile_id = profiles[3]["id"]  # 新しく作成したプロファイルのID
        new_settings = {"input_type": "loopback", "vad_enabled": False}
        result = self.profile_manager.update_profile(profile_id, "更新プロファイル", new_settings)
        self.assertTrue(result)
        
        # プロファイルが更新されたことを確認
        profile = self.profile_manager.get_profile(profile_id)
        self.assertEqual(profile["name"], "更新プロファイル")
        self.assertEqual(profile["settings"], new_settings)
        
    def test_delete_profile(self):
        """プロファイル削除テスト"""
        # プロファイルを作成
        settings = {"input_type": "microphone", "vad_enabled": True}
        self.profile_manager.create_profile("テストプロファイル", settings)
        
        # プロファイルを削除
        profiles = self.profile_manager.list_profiles()
        profile_id = profiles[3]["id"]  # 新しく作成したプロファイルのID
        result = self.profile_manager.delete_profile(profile_id)
        self.assertTrue(result)
        
        # プロファイルが削除されたことを確認
        profiles = self.profile_manager.list_profiles()
        self.assertEqual(len(profiles), 3)  # デフォルト3個のみ
        
    def test_list_profiles(self):
        """プロファイル一覧取得テスト"""
        # デフォルトのプロファイルが作成されていることを確認
        profiles = self.profile_manager.list_profiles()
        self.assertEqual(len(profiles), 3)
        
        # 各プロファイルの内容を確認
        profile_names = [profile["name"] for profile in profiles]
        self.assertIn("会議用", profile_names)
        self.assertIn("メモ用", profile_names)
        self.assertIn("字幕用", profile_names)
        
    def test_get_profile(self):
        """プロファイル取得テスト"""
        # プロファイルを作成
        settings = {"input_type": "microphone", "vad_enabled": True}
        self.profile_manager.create_profile("テストプロファイル", settings)
        
        # プロファイルを取得
        profiles = self.profile_manager.list_profiles()
        profile_id = profiles[3]["id"]  # 新しく作成したプロファイルのID
        profile = self.profile_manager.get_profile(profile_id)
        self.assertIsNotNone(profile)
        self.assertEqual(profile["name"], "テストプロファイル")
        self.assertEqual(profile["settings"], settings)
        
        # 存在しないプロファイルを取得
        profile = self.profile_manager.get_profile(999)
        self.assertIsNone(profile)
        
    def test_get_profile_by_name(self):
        """名前でプロファイル取得テスト"""
        # 名前でプロファイルを取得
        profile = self.profile_manager.get_profile_by_name("会議用")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["name"], "会議用")
        
        # 存在しないプロファイルを取得
        profile = self.profile_manager.get_profile_by_name("存在しないプロファイル")
        self.assertIsNone(profile)


if __name__ == "__main__":
    unittest.main()