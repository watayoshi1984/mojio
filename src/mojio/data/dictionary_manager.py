# -*- coding: utf-8 -*-
"""
User Dictionary Manager for Mojio
Mojio ユーザー辞書管理クラス

ユーザー辞書機能の統合管理クラス
"""

from typing import List, Dict, Optional
from .dictionary_interface import DictionaryInterface
from .user_dictionary import UserDictionary


class DictionaryManager:
    """
    ユーザー辞書機能の統合管理クラス
    
    さまざまなユーザー辞書実装を統一的に管理し、
    アプリケーション全体から簡単に利用できるようにする
    """
    
    def __init__(self):
        """ユーザー辞書管理クラスを初期化"""
        self.current_dictionary: Optional[DictionaryInterface] = None
        self.current_dictionary_type: Optional[str] = None
        self.is_active = False
        
    def initialize_dictionary(self, dictionary_type: str = "user", database_path: str = "data/mojio.db") -> None:
        """
        ユーザー辞書を初期化する
        
        Args:
            dictionary_type: 辞書の種類 ("user" など)
            database_path: データベースファイルのパス
        """
        if dictionary_type == "user":
            self.current_dictionary = UserDictionary()
            self.current_dictionary.initialize(database_path)
            self.current_dictionary_type = dictionary_type
        else:
            raise ValueError(f"サポートされていない辞書タイプ: {dictionary_type}")
            
        self.is_active = True
        
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
        if not self.is_active or self.current_dictionary is None:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize_dictionary()を先に呼び出してください。")
            
        return self.current_dictionary.add_entry(word, reading, category)
        
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
        if not self.is_active or self.current_dictionary is None:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize_dictionary()を先に呼び出してください。")
            
        return self.current_dictionary.update_entry(word, reading, category)
        
    def delete_entry(self, word: str) -> bool:
        """
        辞書からエントリを削除する
        
        Args:
            word: 削除する単語
            
        Returns:
            bool: 削除に成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_active or self.current_dictionary is None:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize_dictionary()を先に呼び出してください。")
            
        return self.current_dictionary.delete_entry(word)
        
    def search_entry(self, word: str) -> Optional[Dict[str, str]]:
        """
        辞書からエントリを検索する
        
        Args:
            word: 検索する単語
            
        Returns:
            Optional[Dict[str, str]]: エントリ情報（見つからない場合はNone）
        """
        if not self.is_active or self.current_dictionary is None:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize_dictionary()を先に呼び出してください。")
            
        return self.current_dictionary.search_entry(word)
        
    def list_entries(self, category: Optional[str] = None) -> List[Dict[str, str]]:
        """
        辞書のエントリ一覧を取得する
        
        Args:
            category: カテゴリでフィルタリング（オプション）
            
        Returns:
            List[Dict[str, str]]: エントリ情報のリスト
        """
        if not self.is_active or self.current_dictionary is None:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize_dictionary()を先に呼び出してください。")
            
        return self.current_dictionary.list_entries(category)
        
    def load_dictionary(self, file_path: str) -> bool:
        """
        ファイルから辞書をロードする
        
        Args:
            file_path: 辞書ファイルのパス
            
        Returns:
            bool: ロードに成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_active or self.current_dictionary is None:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize_dictionary()を先に呼び出してください。")
            
        return self.current_dictionary.load_dictionary(file_path)
        
    def save_dictionary(self, file_path: str) -> bool:
        """
        辞書をファイルに保存する
        
        Args:
            file_path: 保存先ファイルのパス
            
        Returns:
            bool: 保存に成功した場合はTrue、そうでない場合はFalse
        """
        if not self.is_active or self.current_dictionary is None:
            raise RuntimeError("ユーザー辞書が初期化されていません。initialize_dictionary()を先に呼び出してください。")
            
        return self.current_dictionary.save_dictionary(file_path)
        
    def switch_dictionary(self, dictionary_type: str, database_path: str = "data/mojio.db") -> None:
        """
        ユーザー辞書を切り替える
        
        Args:
            dictionary_type: 辞書の種類 ("user" など)
            database_path: データベースファイルのパス
        """
        self.initialize_dictionary(dictionary_type, database_path)