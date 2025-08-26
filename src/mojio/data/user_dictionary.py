# -*- coding: utf-8 -*-
"""
User Dictionary Implementation for Mojio
Mojio ユーザー辞書実装

ユーザー辞書操作の具体実装
"""

import json
import os
from typing import List, Dict, Optional
from .dictionary_interface import DictionaryInterface
from .database_manager import DatabaseManager


class UserDictionary(DictionaryInterface):
    """
    ユーザー辞書操作の具体実装
    
    SQLite3データベースを使用してユーザー辞書の
    登録・編集・削除を行うクラス
    """
    
    def __init__(self):
        """ユーザー辞書を初期化"""
        self.db_manager = DatabaseManager()
        self.is_initialized = False
        self.dictionary_table = "user_dictionary"
        
    def initialize(self, database_path: str = "data/mojio.db") -> None:
        """
        ユーザー辞書を初期化する
        
        Args:
            database_path: データベースファイルのパス
        """
        # データベースを初期化
        self.db_manager.initialize_database("sqlite", database_path)
        
        # ユーザー辞書テーブルを作成
        dictionary_schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "word": "TEXT NOT NULL UNIQUE",
            "reading": "TEXT",
            "category": "TEXT"
        }
        self.db_manager.create_table(self.dictionary_table, dictionary_schema)
        
        self.is_initialized = True
        
    def add_entry(self, word: str, reading: str, category: Optional[str] = None) -> bool:
        """
        辞書にエントリを追加する
        
        Args:
            word: 単語
            reading: 読み（読みがない場合はNone）
            category: カテゴリ（オプション）
            
        Returns:
            bool: 追加に成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_initialized:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースにエントリを挿入
            entry_data = {
                "word": word,
                "reading": reading,
                "category": category
            }
            self.db_manager.insert(self.dictionary_table, entry_data)
            return True
        except Exception as e:
            print(f"エントリの追加に失敗しました: {e}")
            return False
            
    def update_entry(self, word: str, reading: Optional[str] = None, category: Optional[str] = None) -> bool:
        """
        辞書のエントリを更新する
        
        Args:
            word: 更新する単語
            reading: 新しい読み（オプション）
            category: 新しいカテゴリ（オプション）
            
        Returns:
            bool: 更新に成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_initialized:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # 更新するデータを準備
            update_data = {}
            if reading is not None:
                update_data["reading"] = reading
            if category is not None:
                update_data["category"] = category
                
            # データベースのエントリを更新
            if update_data:
                self.db_manager.update(self.dictionary_table, update_data, f"word = '{word}'")
            return True
        except Exception as e:
            print(f"エントリの更新に失敗しました: {e}")
            return False
            
    def delete_entry(self, word: str) -> bool:
        """
        辞書からエントリを削除する
        
        Args:
            word: 削除する単語
            
        Returns:
            bool: 削除に成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_initialized:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースからエントリを削除
            self.db_manager.delete(self.dictionary_table, f"word = '{word}'")
            return True
        except Exception as e:
            print(f"エントリの削除に失敗しました: {e}")
            return False
            
    def search_entry(self, word: str) -> Optional[Dict[str, str]]:
        """
        辞書からエントリを検索する
        
        Args:
            word: 検索する単語
            
        Returns:
            Optional[Dict[str, str]]: エントリ情報（見つからない場合はNone）
        """
        if not self.is_initialized:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースからエントリを検索
            result = self.db_manager.select(self.dictionary_table, ["word", "reading", "category"], f"word = '{word}'")
            if result:
                return result[0]
            return None
        except Exception as e:
            print(f"エントリの検索に失敗しました: {e}")
            return None
            
    def list_entries(self, category: Optional[str] = None) -> List[Dict[str, str]]:
        """
        辞書のエントリ一覧を取得する
        
        Args:
            category: カテゴリでフィルタリング（オプション）
            
        Returns:
            List[Dict[str, str]]: エントリ情報のリスト
        """
        if not self.is_initialized:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # 検索条件を準備
            condition = None
            if category:
                condition = f"category = '{category}'"
                
            # データベースからエントリを検索
            result = self.db_manager.select(self.dictionary_table, ["word", "reading", "category"], condition)
            return result
        except Exception as e:
            print(f"エントリ一覧の取得に失敗しました: {e}")
            return []
            
    def load_dictionary(self, file_path: str) -> bool:
        """
        ファイルから辞書をロードする
        
        Args:
            file_path: 辞書ファイルのパス
            
        Returns:
            bool: ロードに成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_initialized:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # JSONファイルから辞書データをロード
            with open(file_path, 'r', encoding='utf-8') as f:
                dictionary_data = json.load(f)
                
            # データベースにエントリを追加
            for entry in dictionary_data:
                word = entry.get("word")
                reading = entry.get("reading")
                category = entry.get("category")
                
                if word:
                    self.add_entry(word, reading, category)
                    
            return True
        except Exception as e:
            print(f"辞書のロードに失敗しました: {e}")
            return False
            
    def save_dictionary(self, file_path: str) -> bool:
        """
        辞書をファイルに保存する
        
        Args:
            file_path: 保存先ファイルのパス
            
        Returns:
            bool: 保存に成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_initialized:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # データベースからすべてのエントリを取得
            entries = self.list_entries()
            
            # JSONファイルに辞書データを保存
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, ensure_ascii=False, indent=2)
                
            return True
        except Exception as e:
            print(f"辞書の保存に失敗しました: {e}")
            return False