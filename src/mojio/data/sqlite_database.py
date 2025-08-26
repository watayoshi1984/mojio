# -*- coding: utf-8 -*-
"""
SQLite3 Database Implementation for Mojio
Mojio SQLite3データベース実装

SQLite3を使用したデータベース操作の具体実装
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional
from .database_interface import DatabaseInterface


class SQLiteDatabase(DatabaseInterface):
    """
    SQLite3を使用したデータベース操作の具体実装
    
    ユーザー辞書と設定を保存するためのSQLite3データベース操作
    """
    
    def __init__(self):
        """SQLite3データベースを初期化"""
        self.connection: Optional[sqlite3.Connection] = None
        self.database_path: Optional[str] = None
        
    def connect(self, database_path: str) -> None:
        """
        SQLite3データベースに接続する
        
        Args:
            database_path: データベースファイルのパス
        """
        self.database_path = database_path
        
        # データベースファイルのディレクトリが存在しない場合は作成
        db_dir = os.path.dirname(database_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        # データベースに接続
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row  # カラム名でアクセスできるようにする
        
    def disconnect(self) -> None:
        """
        SQLite3データベースから切断する
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.database_path = None
            
    def create_table(self, table_name: str, schema: Dict[str, str]) -> None:
        """
        テーブルを作成する
        
        Args:
            table_name: テーブル名
            schema: テーブルスキーマ（カラム名と型の辞書）
        """
        if not self.connection:
            raise RuntimeError("データベースに接続されていません。connect()を先に呼び出してください。")
            
        # スキーマからCREATE TABLE文を生成
        columns = []
        for column_name, column_type in schema.items():
            columns.append(f"{column_name} {column_type}")
            
        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.connection.execute(create_query)
        self.connection.commit()
        
    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        データを挿入する
        
        Args:
            table_name: テーブル名
            data: 挿入するデータ（カラム名と値の辞書）
            
        Returns:
            int: 挿入されたレコードのID
        """
        if not self.connection:
            raise RuntimeError("データベースに接続されていません。connect()を先に呼び出してください。")
            
        # INSERT文を生成
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # データを挿入
        cursor = self.connection.execute(insert_query, tuple(data.values()))
        self.connection.commit()
        
        # 挿入されたレコードのIDを返す
        return cursor.lastrowid
        
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
        if not self.connection:
            raise RuntimeError("データベースに接続されていません。connect()を先に呼び出してください。")
            
        # UPDATE文を生成
        set_clause = ', '.join([f"{column} = ?" for column in data.keys()])
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        
        # データを更新
        cursor = self.connection.execute(update_query, tuple(data.values()))
        self.connection.commit()
        
        # 更新されたレコード数を返す
        return cursor.rowcount
        
    def delete(self, table_name: str, condition: str) -> int:
        """
        データを削除する
        
        Args:
            table_name: テーブル名
            condition: 削除条件（WHERE句）
            
        Returns:
            int: 削除されたレコード数
        """
        if not self.connection:
            raise RuntimeError("データベースに接続されていません。connect()を先に呼び出してください。")
            
        # DELETE文を生成
        delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        
        # データを削除
        cursor = self.connection.execute(delete_query)
        self.connection.commit()
        
        # 削除されたレコード数を返す
        return cursor.rowcount
        
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
        if not self.connection:
            raise RuntimeError("データベースに接続されていません。connect()を先に呼び出してください。")
            
        # SELECT文を生成
        columns_str = ', '.join(columns)
        select_query = f"SELECT {columns_str} FROM {table_name}"
        if condition:
            select_query += f" WHERE {condition}"
            
        # データを検索
        cursor = self.connection.execute(select_query)
        rows = cursor.fetchall()
        
        # 結果を辞書のリストに変換
        result = []
        for row in rows:
            result.append(dict(row))
            
        return result
        
    def execute(self, query: str, parameters: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        カスタムクエリを実行する
        
        Args:
            query: SQLクエリ
            parameters: クエリパラメータ（オプション）
            
        Returns:
            List[Dict[str, Any]]: クエリ結果のリスト
        """
        if not self.connection:
            raise RuntimeError("データベースに接続されていません。connect()を先に呼び出してください。")
            
        # クエリを実行
        if parameters:
            cursor = self.connection.execute(query, parameters)
        else:
            cursor = self.connection.execute(query)
            
        # SELECTクエリの場合は結果を返す
        query_upper = query.strip().upper()
        if query_upper.startswith("SELECT") or query_upper.startswith("WITH"):
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append(dict(row))
            return result
        else:
            # INSERT/UPDATE/DELETEクエリの場合はコミットして影響を受けた行数を返す
            self.connection.commit()
            return [{"rowcount": cursor.rowcount}]