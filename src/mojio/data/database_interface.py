# -*- coding: utf-8 -*-
"""
Database Interface for Mojio
Mojio データベースインターフェース

データベース操作の抽象インターフェース定義
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class DatabaseInterface(ABC):
    """
    データベース操作の抽象インターフェース
    
    さまざまなデータベース実装を統一的に扱うためのインターフェース
    """
    
    @abstractmethod
    def connect(self, database_path: str) -> None:
        """
        データベースに接続する
        
        Args:
            database_path: データベースファイルのパス
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """
        データベースから切断する
        """
        pass
    
    @abstractmethod
    def create_table(self, table_name: str, schema: Dict[str, str]) -> None:
        """
        テーブルを作成する
        
        Args:
            table_name: テーブル名
            schema: テーブルスキーマ（カラム名と型の辞書）
        """
        pass
    
    @abstractmethod
    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        データを挿入する
        
        Args:
            table_name: テーブル名
            data: 挿入するデータ（カラム名と値の辞書）
            
        Returns:
            int: 挿入されたレコードのID
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete(self, table_name: str, condition: str) -> int:
        """
        データを削除する
        
        Args:
            table_name: テーブル名
            condition: 削除条件（WHERE句）
            
        Returns:
            int: 削除されたレコード数
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def execute(self, query: str, parameters: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        カスタムクエリを実行する
        
        Args:
            query: SQLクエリ
            parameters: クエリパラメータ（オプション）
            
        Returns:
            List[Dict[str, Any]]: クエリ結果のリスト
        """
        pass