# -*- coding: utf-8 -*-
"""
Database Tests for Mojio
Mojio データベーステスト

データベースモジュールのユニットテスト
"""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from mojio.data.database_interface import DatabaseInterface
from mojio.data.sqlite_database import SQLiteDatabase
from mojio.data.database_manager import DatabaseManager


class TestDatabaseInterface:
    """データベースインターフェースのテスト"""
    
    def test_interface_cannot_be_instantiated(self):
        """抽象クラスはインスタンス化できないことを確認"""
        with pytest.raises(TypeError):
            DatabaseInterface()


class TestSQLiteDatabase:
    """SQLiteデータベースのテスト"""
    
    def setup_method(self):
        """テストメソッド実行前のセットアップ"""
        # 一時的なデータベースファイルを作成
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
    def teardown_method(self):
        """テストメソッド実行後のクリーンアップ"""
        # 一時的なデータベースファイルを削除
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
            
    def test_initialization(self):
        """初期化テスト"""
        db = SQLiteDatabase()
        assert db.connection is None
        assert db.database_path is None
        
    def test_connect_and_disconnect(self):
        """接続と切断テスト"""
        db = SQLiteDatabase()
        
        # データベースに接続
        db.connect(self.temp_db.name)
        assert db.connection is not None
        assert db.database_path == self.temp_db.name
        
        # データベースから切断
        db.disconnect()
        assert db.connection is None
        assert db.database_path is None
        
    def test_create_table(self):
        """テーブル作成テスト"""
        db = SQLiteDatabase()
        db.connect(self.temp_db.name)
        
        # テーブルスキーマを定義
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "age": "INTEGER"
        }
        
        # テーブルを作成
        db.create_table("users", schema)
        
        # テーブルが作成されたことを確認
        result = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert len(result) == 1
        assert result[0]["name"] == "users"
        
    def test_insert_and_select(self):
        """データ挿入と検索テスト"""
        db = SQLiteDatabase()
        db.connect(self.temp_db.name)
        
        # テーブルを作成
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "age": "INTEGER"
        }
        db.create_table("users", schema)
        
        # データを挿入
        user_data = {"name": "テスト太郎", "age": 30}
        inserted_id = db.insert("users", user_data)
        assert inserted_id == 1
        
        # データを検索
        result = db.select("users", ["id", "name", "age"])
        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["name"] == "テスト太郎"
        assert result[0]["age"] == 30
        
    def test_update(self):
        """データ更新テスト"""
        db = SQLiteDatabase()
        db.connect(self.temp_db.name)
        
        # テーブルを作成
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "age": "INTEGER"
        }
        db.create_table("users", schema)
        
        # データを挿入
        user_data = {"name": "テスト太郎", "age": 30}
        db.insert("users", user_data)
        
        # データを更新
        update_data = {"name": "テスト次郎", "age": 35}
        updated_count = db.update("users", update_data, "id = 1")
        assert updated_count == 1
        
        # データが更新されたことを確認
        result = db.select("users", ["id", "name", "age"], "id = 1")
        assert len(result) == 1
        assert result[0]["name"] == "テスト次郎"
        assert result[0]["age"] == 35
        
    def test_delete(self):
        """データ削除テスト"""
        db = SQLiteDatabase()
        db.connect(self.temp_db.name)
        
        # テーブルを作成
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "age": "INTEGER"
        }
        db.create_table("users", schema)
        
        # データを挿入
        user_data = {"name": "テスト太郎", "age": 30}
        db.insert("users", user_data)
        
        # データを削除
        deleted_count = db.delete("users", "id = 1")
        assert deleted_count == 1
        
        # データが削除されたことを確認
        result = db.select("users", ["id", "name", "age"])
        assert len(result) == 0
        
    def test_execute_select_query(self):
        """SELECTクエリ実行テスト"""
        db = SQLiteDatabase()
        db.connect(self.temp_db.name)
        
        # テーブルを作成
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "age": "INTEGER"
        }
        db.create_table("users", schema)
        
        # データを挿入
        user_data = {"name": "テスト太郎", "age": 30}
        db.insert("users", user_data)
        
        # カスタムSELECTクエリを実行
        result = db.execute("SELECT * FROM users WHERE age > ?", (25,))
        assert len(result) == 1
        assert result[0]["name"] == "テスト太郎"
        assert result[0]["age"] == 30
        
    def test_execute_insert_query(self):
        """INSERTクエリ実行テスト"""
        db = SQLiteDatabase()
        db.connect(self.temp_db.name)
        
        # テーブルを作成
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "age": "INTEGER"
        }
        db.create_table("users", schema)
        
        # カスタムINSERTクエリを実行
        result = db.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("テスト太郎", 30))
        assert result[0]["rowcount"] == 1
        
        # データが挿入されたことを確認
        select_result = db.select("users", ["id", "name", "age"])
        assert len(select_result) == 1
        assert select_result[0]["name"] == "テスト太郎"
        assert select_result[0]["age"] == 30


class TestDatabaseManager:
    """データベース管理のテスト"""
    
    def setup_method(self):
        """テストメソッド実行前のセットアップ"""
        # 一時的なデータベースファイルを作成
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
    def teardown_method(self):
        """テストメソッド実行後のクリーンアップ"""
        # 一時的なデータベースファイルを削除
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
            
    def test_initialization(self):
        """初期化テスト"""
        manager = DatabaseManager()
        assert manager.current_database is None
        assert manager.current_database_type is None
        assert manager.is_active is False
        assert manager.database_path is None
        
    def test_initialize_database(self):
        """データベース初期化テスト"""
        manager = DatabaseManager()
        manager.initialize_database(database_type="sqlite", database_path=self.temp_db.name)
        
        assert isinstance(manager.current_database, SQLiteDatabase)
        assert manager.current_database_type == "sqlite"
        assert manager.is_active is True
        assert manager.database_path == self.temp_db.name
        
    def test_initialize_database_invalid_type(self):
        """無効なデータベースタイプでの初期化テスト"""
        manager = DatabaseManager()
        
        with pytest.raises(ValueError, match="サポートされていないデータベースタイプ"):
            manager.initialize_database(database_type="invalid_type", database_path=self.temp_db.name)
            
    def test_disconnect(self):
        """切断テスト"""
        manager = DatabaseManager()
        manager.initialize_database(database_type="sqlite", database_path=self.temp_db.name)
        assert manager.is_active is True
        
        manager.disconnect()
        assert manager.is_active is False
        assert manager.database_path is None
        
    @patch('mojio.data.sqlite_database.SQLiteDatabase')
    def test_create_table(self, mock_sqlite_class):
        """テーブル作成テスト"""
        mock_sqlite_instance = Mock()
        mock_sqlite_class.return_value = mock_sqlite_instance
        
        manager = DatabaseManager()
        manager.initialize_database(database_type="sqlite", database_path=self.temp_db.name)
        
        schema = {"id": "INTEGER PRIMARY KEY", "name": "TEXT"}
        manager.create_table("users", schema)
        
        mock_sqlite_instance.create_table.assert_called_once_with("users", schema)
        
    @patch('mojio.data.sqlite_database.SQLiteDatabase')
    def test_insert(self, mock_sqlite_class):
        """データ挿入テスト"""
        mock_sqlite_instance = Mock()
        mock_sqlite_instance.insert.return_value = 1
        mock_sqlite_class.return_value = mock_sqlite_instance
        
        manager = DatabaseManager()
        manager.initialize_database(database_type="sqlite", database_path=self.temp_db.name)
        
        data = {"name": "テスト太郎", "age": 30}
        result = manager.insert("users", data)
        
        assert result == 1
        mock_sqlite_instance.insert.assert_called_once_with("users", data)
        
    @patch('mojio.data.sqlite_database.SQLiteDatabase')
    def test_update(self, mock_sqlite_class):
        """データ更新テスト"""
        mock_sqlite_instance = Mock()
        mock_sqlite_instance.update.return_value = 1
        mock_sqlite_class.return_value = mock_sqlite_instance
        
        manager = DatabaseManager()
        manager.initialize_database(database_type="sqlite", database_path=self.temp_db.name)
        
        data = {"name": "テスト次郎", "age": 35}
        result = manager.update("users", data, "id = 1")
        
        assert result == 1
        mock_sqlite_instance.update.assert_called_once_with("users", data, "id = 1")
        
    @patch('mojio.data.sqlite_database.SQLiteDatabase')
    def test_delete(self, mock_sqlite_class):
        """データ削除テスト"""
        mock_sqlite_instance = Mock()
        mock_sqlite_instance.delete.return_value = 1
        mock_sqlite_class.return_value = mock_sqlite_instance
        
        manager = DatabaseManager()
        manager.initialize_database(database_type="sqlite", database_path=self.temp_db.name)
        
        result = manager.delete("users", "id = 1")
        
        assert result == 1
        mock_sqlite_instance.delete.assert_called_once_with("users", "id = 1")
        
    @patch('mojio.data.sqlite_database.SQLiteDatabase')
    def test_select(self, mock_sqlite_class):
        """データ検索テスト"""
        mock_sqlite_instance = Mock()
        mock_sqlite_instance.select.return_value = [{"id": 1, "name": "テスト太郎", "age": 30}]
        mock_sqlite_class.return_value = mock_sqlite_instance
        
        manager = DatabaseManager()
        manager.initialize_database(database_type="sqlite", database_path=self.temp_db.name)
        
        result = manager.select("users", ["id", "name", "age"], "id = 1")
        
        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["name"] == "テスト太郎"
        assert result[0]["age"] == 30
        mock_sqlite_instance.select.assert_called_once_with("users", ["id", "name", "age"], "id = 1")
        
    @patch('mojio.data.sqlite_database.SQLiteDatabase')
    def test_execute(self, mock_sqlite_class):
        """カスタムクエリ実行テスト"""
        mock_sqlite_instance = Mock()
        mock_sqlite_instance.execute.return_value = [{"id": 1, "name": "テスト太郎", "age": 30}]
        mock_sqlite_class.return_value = mock_sqlite_instance
        
        manager = DatabaseManager()
        manager.initialize_database(database_type="sqlite", database_path=self.temp_db.name)
        
        result = manager.execute("SELECT * FROM users WHERE id = ?", (1,))
        
        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["name"] == "テスト太郎"
        assert result[0]["age"] == 30
        mock_sqlite_instance.execute.assert_called_once_with("SELECT * FROM users WHERE id = ?", (1,))


if __name__ == "__main__":
    pytest.main([__file__])