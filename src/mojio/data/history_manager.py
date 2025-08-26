# -*- coding: utf-8 -*-
"""
History Manager Implementation for Mojio
Mojio 履歴管理実装

データベースを使用した履歴管理の具体実装
"""

from typing import List, Dict, Optional
from datetime import datetime
from .history_interface import HistoryInterface
from .database_manager import DatabaseManager


class HistoryManager(HistoryInterface):
    """
    履歴管理の具体実装クラス
    
    SQLite3データベースを使用して文字起こし結果の
    保存・検索・削除を行う機能を提供する
    """
    
    def __init__(self):
        """履歴管理を初期化"""
        self.db_manager = DatabaseManager()
        self.is_initialized = False
        self.history_table = "transcription_history"
        
    def initialize(self, database_path: str = "data/mojio.db") -> None:
        """
        履歴管理を初期化する
        
        Args:
            database_path: データベースファイルのパス
        """
        # データベースを初期化
        self.db_manager.initialize_database("sqlite", database_path)
        
        # 履歴テーブルを作成
        history_schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "text": "TEXT NOT NULL",
            "timestamp": "TEXT",
            "speaker": "TEXT"
        }
        self.db_manager.create_table(self.history_table, history_schema)
        
        self.is_initialized = True
        
    def add_entry(self, text: str, timestamp: Optional[str] = None, speaker: Optional[str] = None) -> bool:
        """
        履歴にエントリを追加する
        
        Args:
            text: 文字起こし結果
            timestamp: タイムスタンプ（オプション）
            speaker: 話者情報（オプション）
            
        Returns:
            bool: 追加に成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_initialized:
            raise RuntimeError("履歴管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # タイムスタンプが指定されていない場合は現在時刻を使用
            if timestamp is None:
                timestamp = datetime.now().isoformat()
                
            # データベースにエントリを挿入
            entry_data = {
                "text": text,
                "timestamp": timestamp,
                "speaker": speaker
            }
            self.db_manager.insert(self.history_table, entry_data)
            return True
        except Exception as e:
            print(f"エントリの追加に失敗しました: {e}")
            return False
            
    def delete_entry(self, entry_id: int) -> bool:
        """
        履歴からエントリを削除する
        
        Args:
            entry_id: エントリID
            
        Returns:
            bool: 削除に成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_initialized:
            raise RuntimeError("履歴管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースからエントリを削除
            self.db_manager.delete(self.history_table, f"id = {entry_id}")
            return True
        except Exception as e:
            print(f"エントリの削除に失敗しました: {e}")
            return False
            
    def search_entries(self, keyword: str, limit: int = 100) -> List[Dict[str, any]]:
        """
        履歴からエントリを検索する
        
        Args:
            keyword: 検索キーワード
            limit: 検索結果の上限数
            
        Returns:
            List[Dict[str, any]]: エントリ情報のリスト
        """
        if not self.is_initialized:
            raise RuntimeError("履歴管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースからエントリを検索
            query = f"SELECT id, text, timestamp, speaker FROM {self.history_table} WHERE text LIKE ? ORDER BY timestamp DESC LIMIT ?"
            result = self.db_manager.execute(query, (f"%{keyword}%", limit))
            return result
        except Exception as e:
            print(f"エントリの検索に失敗しました: {e}")
            return []
            
    def list_entries(self, limit: int = 100) -> List[Dict[str, any]]:
        """
        履歴のエントリ一覧を取得する
        
        Args:
            limit: 取得するエントリ数の上限
            
        Returns:
            List[Dict[str, any]]: エントリ情報のリスト
        """
        if not self.is_initialized:
            raise RuntimeError("履歴管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースからエントリを取得
            query = f"SELECT id, text, timestamp, speaker FROM {self.history_table} ORDER BY timestamp DESC LIMIT ?"
            result = self.db_manager.execute(query, (limit,))
            return result
        except Exception as e:
            print(f"エントリ一覧の取得に失敗しました: {e}")
            return []
            
    def get_entry(self, entry_id: int) -> Optional[Dict[str, any]]:
        """
        IDでエントリを取得する
        
        Args:
            entry_id: エントリID
            
        Returns:
            Optional[Dict[str, any]]: エントリ情報（見つからない場合はNone）
        """
        if not self.is_initialized:
            raise RuntimeError("履歴管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースからエントリを取得
            query = f"SELECT id, text, timestamp, speaker FROM {self.history_table} WHERE id = ?"
            result = self.db_manager.execute(query, (entry_id,))
            if result:
                return result[0]
            return None
        except Exception as e:
            print(f"エントリの取得に失敗しました: {e}")
            return None