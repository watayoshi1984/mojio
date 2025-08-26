# -*- coding: utf-8 -*-
"""
Profile Manager Implementation for Mojio
Mojio プロファイル管理実装

データベースを使用したプロファイル管理の具体実装
"""

import json
from typing import List, Dict, Optional
from .profile_interface import ProfileInterface
from .database_manager import DatabaseManager


class ProfileManager(ProfileInterface):
    """
    プロファイル管理の具体実装クラス
    
    SQLite3データベースを使用してプロファイルの
    作成・編集・削除・取得を行う機能を提供する
    """
    
    def __init__(self):
        """プロファイル管理を初期化"""
        self.db_manager = DatabaseManager()
        self.is_initialized = False
        self.profile_table = "profiles"
        
    def initialize(self, database_path: str = "data/mojio.db") -> None:
        """
        プロファイル管理を初期化する
        
        Args:
            database_path: データベースファイルのパス
        """
        # データベースを初期化
        self.db_manager.initialize_database("sqlite", database_path)
        
        # プロファイルテーブルを作成
        profile_schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL UNIQUE",
            "settings": "TEXT"
        }
        self.db_manager.create_table(self.profile_table, profile_schema)
        
        self.is_initialized = True
        
        # デフォルトプロファイルを作成
        self._create_default_profiles()
        
    def _create_default_profiles(self) -> None:
        """デフォルトプロファイルを作成する"""
        # 会議用プロファイル
        meeting_settings = {
            "input_type": "microphone",
            "vad_enabled": True,
            "speaker_detection_enabled": True,
            "punctuation_enabled": True,
            "history_enabled": True
        }
        self.create_profile("会議用", meeting_settings)
        
        # メモ用プロファイル
        memo_settings = {
            "input_type": "microphone",
            "vad_enabled": True,
            "speaker_detection_enabled": False,
            "punctuation_enabled": False,
            "history_enabled": True
        }
        self.create_profile("メモ用", memo_settings)
        
        # 字幕用プロファイル
        subtitle_settings = {
            "input_type": "loopback",
            "vad_enabled": True,
            "speaker_detection_enabled": False,
            "punctuation_enabled": True,
            "history_enabled": True
        }
        self.create_profile("字幕用", subtitle_settings)
        
    def create_profile(self, name: str, settings: Dict[str, any]) -> bool:
        """
        プロファイルを作成する
        
        Args:
            name: プロファイル名
            settings: 設定情報
            
        Returns:
            bool: 作成に成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_initialized:
            raise RuntimeError("プロファイル管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # 設定情報をJSON文字列に変換
            settings_json = json.dumps(settings, ensure_ascii=False)
            
            # データベースにプロファイルを挿入
            profile_data = {
                "name": name,
                "settings": settings_json
            }
            self.db_manager.insert(self.profile_table, profile_data)
            return True
        except Exception as e:
            print(f"プロファイルの作成に失敗しました: {e}")
            return False
            
    def update_profile(self, profile_id: int, name: Optional[str] = None, settings: Optional[Dict[str, any]] = None) -> bool:
        """
        プロファイルを更新する
        
        Args:
            profile_id: プロファイルID
            name: 新しいプロファイル名（オプション）
            settings: 新しい設定情報（オプション）
            
        Returns:
            bool: 更新に成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_initialized:
            raise RuntimeError("プロファイル管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # 更新するデータを準備
            update_data = {}
            if name is not None:
                update_data["name"] = name
            if settings is not None:
                update_data["settings"] = json.dumps(settings, ensure_ascii=False)
                
            # データベースのプロファイルを更新
            if update_data:
                self.db_manager.update(self.profile_table, update_data, f"id = {profile_id}")
            return True
        except Exception as e:
            print(f"プロファイルの更新に失敗しました: {e}")
            return False
            
    def delete_profile(self, profile_id: int) -> bool:
        """
        プロファイルを削除する
        
        Args:
            profile_id: プロファイルID
            
        Returns:
            bool: 削除に成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_initialized:
            raise RuntimeError("プロファイル管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースからプロファイルを削除
            self.db_manager.delete(self.profile_table, f"id = {profile_id}")
            return True
        except Exception as e:
            print(f"プロファイルの削除に失敗しました: {e}")
            return False
            
    def list_profiles(self) -> List[Dict[str, any]]:
        """
        プロファイル一覧を取得する
        
        Returns:
            List[Dict[str, any]]: プロファイル情報のリスト
        """
        if not self.is_initialized:
            raise RuntimeError("プロファイル管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースからプロファイルを取得
            result = self.db_manager.select(self.profile_table, ["id", "name", "settings"])
            
            # 設定情報をJSONから辞書に変換
            for profile in result:
                if profile["settings"]:
                    profile["settings"] = json.loads(profile["settings"])
                    
            return result
        except Exception as e:
            print(f"プロファイル一覧の取得に失敗しました: {e}")
            return []
            
    def get_profile(self, profile_id: int) -> Optional[Dict[str, any]]:
        """
        IDでプロファイルを取得する
        
        Args:
            profile_id: プロファイルID
            
        Returns:
            Optional[Dict[str, any]]: プロファイル情報（見つからない場合はNone）
        """
        if not self.is_initialized:
            raise RuntimeError("プロファイル管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースからプロファイルを取得
            result = self.db_manager.select(self.profile_table, ["id", "name", "settings"], f"id = {profile_id}")
            if result:
                profile = result[0]
                # 設定情報をJSONから辞書に変換
                if profile["settings"]:
                    profile["settings"] = json.loads(profile["settings"])
                return profile
            return None
        except Exception as e:
            print(f"プロファイルの取得に失敗しました: {e}")
            return None
            
    def get_profile_by_name(self, name: str) -> Optional[Dict[str, any]]:
        """
        名前でプロファイルを取得する
        
        Args:
            name: プロファイル名
            
        Returns:
            Optional[Dict[str, any]]: プロファイル情報（見つからない場合はNone）
        """
        if not self.is_initialized:
            raise RuntimeError("プロファイル管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースからプロファイルを取得
            result = self.db_manager.select(self.profile_table, ["id", "name", "settings"], f"name = '{name}'")
            if result:
                profile = result[0]
                # 設定情報をJSONから辞書に変換
                if profile["settings"]:
                    profile["settings"] = json.loads(profile["settings"])
                return profile
            return None
        except Exception as e:
            print(f"プロファイルの取得に失敗しました: {e}")
            return None