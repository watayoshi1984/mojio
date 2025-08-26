# -*- coding: utf-8 -*-
"""
Database Manager for Mojio
Mojio データベース管理クラス

データベース機能の統合管理クラス
"""

from typing import List, Dict, Any, Optional
from .database_interface import DatabaseInterface
from .sqlite_database import SQLiteDatabase


class DatabaseManager:
    """
    データベース機能の統合管理クラス
    
    さまざまなデータベース実装を統一的に管理し、
    アプリケーション全体から簡単に利用できるようにする
    """
    
    def __init__(self):
        """データベース管理クラスを初期化"""
        self.current_database: Optional[DatabaseInterface] = None
        self.current_database_type: Optional[str] = None
        self.is_active = False
        self.database_path: Optional[str] = None
        
    def initialize_database(self, database_type: str = "sqlite", database_path: str = "data/mojio.db") -> None:
        """
        データベースを初期化する
        
        Args:
            database_type: データベースの種類 ("sqlite" など)
            database_path: データベースファイルのパス
        """
        self.database_path = database_path
        
        if database_type == "sqlite":
            self.current_database = SQLiteDatabase()
            self.current_database_type = database_type
        else:
            raise ValueError(f"サポートされていないデータベースタイプ: {database_type}")
            
        # データベースに接続
        self.current_database.connect(database_path)
        self.is_active = True
        
    def disconnect(self) -> None:
        """
        データベースから切断する
        """
        if not self.is_active or self.current_database is None:
            return
            
        self.current_database.disconnect()
        self.is_active = False
        self.database_path = None
        
    def create_table(self, table_name: str, schema: Dict[str, str]) -> None:
        """
        テーブルを作成する
        
        Args:
            table_name: テーブル名
            schema: テーブルスキーマ（カラム名と型の辞書）
        """
        if not self.is_active or self.current_database is None:
            raise RuntimeError("データベースが初期化されていません。initialize_database()を先に呼び出してください。")
            
        self.current_database.create_table(table_name, schema)
        
    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        データを挿入する
        
        Args:
            table_name: テーブル名
            data: 挿入するデータ（カラム名と値の辞書）
            
        Returns:
            int: 挿入されたレコードのID
        """
        if not self.is_active or self.current_database is None:
            raise RuntimeError("データベースが初期化されていません。initialize_database()を先に呼び出してください。")
            
        return self.current_database.insert(table_name, data)
        
    def update(self, table_name: str, data: Dict[str, Any], condition: str) -> int:
        """
        データを更新する
        
        Args:
            table_name: テーブル名
            data: 更新するデータ（カラム名と値の辞書）
            condition: 更新条件（WHERE句）
            
        Returns:
            int: 更新されたレコード数
        """
        if not self.is_active or self.current_database is None:
            raise RuntimeError("データベースが初期化されていません。initialize_database()を先に呼び出してください。")
            
        return self.current_database.update(table_name, data, condition)
        
    def delete(self, table_name: str, condition: str) -> int:
        """
        データを削除する
        
        Args:
            table_name: テーブル名
            condition: 削除条件（WHERE句）
            
        Returns:
            int: 削除されたレコード数
        """
        if not self.is_active or self.current_database is None:
            raise RuntimeError("データベースが初期化されていません。initialize_database()を先に呼び出してください。")
            
        return self.current_database.delete(table_name, condition)
        
    def select(self, table_name: str, columns: List[str], condition: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        データを検索する
        
        Args:
            table_name: テーブル名
            columns: 取得するカラム名のリスト
            condition: 検索条件（WHERE句、オプション）
            
        Returns:
            List[Dict[str, Any]]: 検索結果のリスト
        """
        if not self.is_active or self.current_database is None:
            raise RuntimeError("データベースが初期化されていません。initialize_database()を先に呼び出してください。")
            
        return self.current_database.select(table_name, columns, condition)
        
    def execute(self, query: str, parameters: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        カスタムクエリを実行する
        
        Args:
            query: SQLクエリ
            parameters: クエリパラメータ（オプション）
            
        Returns:
            List[Dict[str, Any]]: クエリ結果のリスト
        """
        if not self.is_active or self.current_database is None:
            raise RuntimeError("データベースが初期化されていません。initialize_database()を先に呼び出してください。")
            
        return self.current_database.execute(query, parameters)
        
    def switch_database(self, database_type: str, database_path: str) -> None:
        """
        データベースを切り替える
        
        Args:
            database_type: データベースの種類 ("sqlite" など)
            database_path: データベースファイルのパス
        """
        # 現在のデータベースから切断
        if self.is_active:
            self.disconnect()
            
        # 新しいデータベースを初期化
        self.initialize_database(database_type, database_path)