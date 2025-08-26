# -*- coding: utf-8 -*-
"""
User Dictionary Tests for Mojio
Mojio ユーザー辞書テスト

ユーザー辞書モジュールのユニットテスト
"""

import pytest
import os
import tempfile
import json
from unittest.mock import Mock, patch
from mojio.data.dictionary_interface import DictionaryInterface
from mojio.data.user_dictionary import UserDictionary
from mojio.data.dictionary_manager import DictionaryManager


class TestDictionaryInterface:
    """ユーザー辞書インターフェースのテスト"""
    
    def test_interface_cannot_be_instantiated(self):
        """抽象クラスはインスタンス化できないことを確認"""
        with pytest.raises(TypeError):
            DictionaryInterface()


class TestUserDictionary:
    """ユーザー辞書のテスト"""
    
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
        dictionary = UserDictionary()
        dictionary.initialize(self.temp_db.name)
        
        assert dictionary.is_initialized is True
        
    def test_add_entry(self):
        """エントリ追加テスト"""
        dictionary = UserDictionary()
        dictionary.initialize(self.temp_db.name)
        
        # エントリを追加
        result = dictionary.add_entry("テスト", "てすと", "一般")
        assert result is True
        
        # エントリが追加されたことを確認
        entry = dictionary.search_entry("テスト")
        assert entry is not None
        assert entry["word"] == "テスト"
        assert entry["reading"] == "てすと"
        assert entry["category"] == "一般"
        
    def test_update_entry(self):
        """エントリ更新テスト"""
        dictionary = UserDictionary()
        dictionary.initialize(self.temp_db.name)
        
        # エントリを追加
        dictionary.add_entry("テスト", "てすと", "一般")
        
        # エントリを更新
        result = dictionary.update_entry("テスト", reading="テストです", category="名詞")
        assert result is True
        
        # エントリが更新されたことを確認
        entry = dictionary.search_entry("テスト")
        assert entry is not None
        assert entry["word"] == "テスト"
        assert entry["reading"] == "テストです"
        assert entry["category"] == "名詞"
        
    def test_delete_entry(self):
        """エントリ削除テスト"""
        dictionary = UserDictionary()
        dictionary.initialize(self.temp_db.name)
        
        # エントリを追加
        dictionary.add_entry("テスト", "てすと", "一般")
        
        # エントリを削除
        result = dictionary.delete_entry("テスト")
        assert result is True
        
        # エントリが削除されたことを確認
        entry = dictionary.search_entry("テスト")
        assert entry is None
        
    def test_search_entry_not_found(self):
        """エントリ検索（見つからない場合）テスト"""
        dictionary = UserDictionary()
        dictionary.initialize(self.temp_db.name)
        
        # 存在しないエントリを検索
        entry = dictionary.search_entry("存在しない")
        assert entry is None
        
    def test_list_entries(self):
        """エントリ一覧取得テスト"""
        dictionary = UserDictionary()
        dictionary.initialize(self.temp_db.name)
        
        # 複数のエントリを追加
        dictionary.add_entry("テスト1", "てすと1", "一般")
        dictionary.add_entry("テスト2", "てすと2", "固有名詞")
        dictionary.add_entry("テスト3", "てすと3", "一般")
        
        # すべてのエントリを取得
        entries = dictionary.list_entries()
        assert len(entries) == 3
        
        # カテゴリでフィルタリング
        general_entries = dictionary.list_entries("一般")
        assert len(general_entries) == 2
        
    def test_load_dictionary(self):
        """辞書ロードテスト"""
        dictionary = UserDictionary()
        dictionary.initialize(self.temp_db.name)
        
        # 一時的なJSONファイルを作成
        temp_json = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_json.close()
        
        try:
            # テストデータを作成
            test_data = [
                {"word": "ロードテスト1", "reading": "ろーどてすと1", "category": "一般"},
                {"word": "ロードテスト2", "reading": "ろーどてすと2", "category": "固有名詞"}
            ]
            
            # JSONファイルにテストデータを書き込み
            with open(temp_json.name, 'w', encoding='utf-8') as f:
                json.dump(test_data, f, ensure_ascii=False, indent=2)
                
            # 辞書をロード
            result = dictionary.load_dictionary(temp_json.name)
            assert result is True
            
            # エントリがロードされたことを確認
            entry1 = dictionary.search_entry("ロードテスト1")
            assert entry1 is not None
            assert entry1["word"] == "ロードテスト1"
            assert entry1["reading"] == "ろーどてすと1"
            assert entry1["category"] == "一般"
            
            entry2 = dictionary.search_entry("ロードテスト2")
            assert entry2 is not None
            assert entry2["word"] == "ロードテスト2"
            assert entry2["reading"] == "ろーどてすと2"
            assert entry2["category"] == "固有名詞"
            
        finally:
            # 一時的なJSONファイルを削除
            if os.path.exists(temp_json.name):
                os.unlink(temp_json.name)
                
    def test_save_dictionary(self):
        """辞書保存テスト"""
        dictionary = UserDictionary()
        dictionary.initialize(self.temp_db.name)
        
        # エントリを追加
        dictionary.add_entry("保存テスト1", "ほぞんてすと1", "一般")
        dictionary.add_entry("保存テスト2", "ほぞんてすと2", "固有名詞")
        
        # 一時的なJSONファイルを作成
        temp_json = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_json.close()
        
        try:
            # 辞書を保存
            result = dictionary.save_dictionary(temp_json.name)
            assert result is True
            
            # 保存されたファイルからデータを読み込み
            with open(temp_json.name, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                
            # データが正しく保存されたことを確認
            assert len(saved_data) == 2
            words = [entry["word"] for entry in saved_data]
            assert "保存テスト1" in words
            assert "保存テスト2" in words
            
        finally:
            # 一時的なJSONファイルを削除
            if os.path.exists(temp_json.name):
                os.unlink(temp_json.name)


class TestDictionaryManager:
    """ユーザー辞書管理のテスト"""
    
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
        manager = DictionaryManager()
        manager.initialize_dictionary(dictionary_type="user", database_path=self.temp_db.name)
        
        assert isinstance(manager.current_dictionary, UserDictionary)
        assert manager.current_dictionary_type == "user"
        assert manager.is_active is True
        
    def test_initialization_invalid_type(self):
        """無効な辞書タイプでの初期化テスト"""
        manager = DictionaryManager()
        
        with pytest.raises(ValueError, match="サポートされていない辞書タイプ"):
            manager.initialize_dictionary(dictionary_type="invalid_type", database_path=self.temp_db.name)
            
    @patch('mojio.data.user_dictionary.UserDictionary')
    def test_add_entry(self, mock_user_dict_class):
        """エントリ追加テスト"""
        mock_user_dict_instance = Mock()
        mock_user_dict_instance.add_entry.return_value = True
        mock_user_dict_class.return_value = mock_user_dict_instance
        
        manager = DictionaryManager()
        manager.initialize_dictionary(dictionary_type="user", database_path=self.temp_db.name)
        
        result = manager.add_entry("テスト", "てすと", "一般")
        assert result is True
        mock_user_dict_instance.add_entry.assert_called_once_with("テスト", "てすと", "一般")
        
    @patch('mojio.data.user_dictionary.UserDictionary')
    def test_update_entry(self, mock_user_dict_class):
        """エントリ更新テスト"""
        mock_user_dict_instance = Mock()
        mock_user_dict_instance.update_entry.return_value = True
        mock_user_dict_class.return_value = mock_user_dict_instance
        
        manager = DictionaryManager()
        manager.initialize_dictionary(dictionary_type="user", database_path=self.temp_db.name)
        
        result = manager.update_entry("テスト", reading="テストです", category="名詞")
        assert result is True
        mock_user_dict_instance.update_entry.assert_called_once_with("テスト", reading="テストです", category="名詞")
        
    @patch('mojio.data.user_dictionary.UserDictionary')
    def test_delete_entry(self, mock_user_dict_class):
        """エントリ削除テスト"""
        mock_user_dict_instance = Mock()
        mock_user_dict_instance.delete_entry.return_value = True
        mock_user_dict_class.return_value = mock_user_dict_instance
        
        manager = DictionaryManager()
        manager.initialize_dictionary(dictionary_type="user", database_path=self.temp_db.name)
        
        result = manager.delete_entry("テスト")
        assert result is True
        mock_user_dict_instance.delete_entry.assert_called_once_with("テスト")
        
    @patch('mojio.data.user_dictionary.UserDictionary')
    def test_search_entry(self, mock_user_dict_class):
        """エントリ検索テスト"""
        mock_user_dict_instance = Mock()
        mock_user_dict_instance.search_entry.return_value = {"word": "テスト", "reading": "てすと", "category": "一般"}
        mock_user_dict_class.return_value = mock_user_dict_instance
        
        manager = DictionaryManager()
        manager.initialize_dictionary(dictionary_type="user", database_path=self.temp_db.name)
        
        result = manager.search_entry("テスト")
        assert result is not None
        assert result["word"] == "テスト"
        assert result["reading"] == "てすと"
        assert result["category"] == "一般"
        mock_user_dict_instance.search_entry.assert_called_once_with("テスト")
        
    @patch('mojio.data.user_dictionary.UserDictionary')
    def test_list_entries(self, mock_user_dict_class):
        """エントリ一覧取得テスト"""
        mock_user_dict_instance = Mock()
        mock_user_dict_instance.list_entries.return_value = [
            {"word": "テスト1", "reading": "てすと1", "category": "一般"},
            {"word": "テスト2", "reading": "てすと2", "category": "固有名詞"}
        ]
        mock_user_dict_class.return_value = mock_user_dict_instance
        
        manager = DictionaryManager()
        manager.initialize_dictionary(dictionary_type="user", database_path=self.temp_db.name)
        
        result = manager.list_entries("一般")
        assert len(result) == 2
        assert result[0]["word"] == "テスト1"
        assert result[1]["word"] == "テスト2"
        mock_user_dict_instance.list_entries.assert_called_once_with("一般")
        
    @patch('mojio.data.user_dictionary.UserDictionary')
    def test_load_dictionary(self, mock_user_dict_class):
        """辞書ロードテスト"""
        mock_user_dict_instance = Mock()
        mock_user_dict_instance.load_dictionary.return_value = True
        mock_user_dict_class.return_value = mock_user_dict_instance
        
        manager = DictionaryManager()
        manager.initialize_dictionary(dictionary_type="user", database_path=self.temp_db.name)
        
        result = manager.load_dictionary("test_dict.json")
        assert result is True
        mock_user_dict_instance.load_dictionary.assert_called_once_with("test_dict.json")
        
    @patch('mojio.data.user_dictionary.UserDictionary')
    def test_save_dictionary(self, mock_user_dict_class):
        """辞書保存テスト"""
        mock_user_dict_instance = Mock()
        mock_user_dict_instance.save_dictionary.return_value = True
        mock_user_dict_class.return_value = mock_user_dict_instance
        
        manager = DictionaryManager()
        manager.initialize_dictionary(dictionary_type="user", database_path=self.temp_db.name)
        
        result = manager.save_dictionary("test_dict.json")
        assert result is True
        mock_user_dict_instance.save_dictionary.assert_called_once_with("test_dict.json")


if __name__ == "__main__":
    pytest.main([__file__])