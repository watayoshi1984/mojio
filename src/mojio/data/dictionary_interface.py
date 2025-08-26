# -*- coding: utf-8 -*-
"""
User Dictionary Interface for Mojio
Mojio ユーザー辞書インターフェース

ユーザー辞書操作の抽象インターフェース定義
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class DictionaryInterface(ABC):
    """
    ユーザー辞書操作の抽象インターフェース
    
    さまざまなユーザー辞書実装を統一的に扱うためのインターフェース
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete_entry(self, word: str) -> bool:
        """
        辞書からエントリを削除する
        
        Args:
            word: 削除する単語
            
        Returns:
            bool: 削除に成功した場合はTrue、そうでない場合はFalse
        """
        pass
    
    @abstractmethod
    def search_entry(self, word: str) -> Optional[Dict[str, str]]:
        """
        辞書からエントリを検索する
        
        Args:
            word: 検索する単語
            
        Returns:
            Optional[Dict[str, str]]: エントリ情報（見つからない場合はNone）
        """
        pass
    
    @abstractmethod
    def list_entries(self, category: Optional[str] = None) -> List[Dict[str, str]]:
        """
        辞書のエントリ一覧を取得する
        
        Args:
            category: カテゴリでフィルタリング（オプション）
            
        Returns:
            List[Dict[str, str]]: エントリ情報のリスト
        """
        pass
    
    @abstractmethod
    def load_dictionary(self, file_path: str) -> bool:
        """
        ファイルから辞書をロードする
        
        Args:
            file_path: 辞書ファイルのパス
            
        Returns:
            bool: ロードに成功した場合はTrue、そうでない場合はFalse
        """
        pass
    
    @abstractmethod
    def save_dictionary(self, file_path: str) -> bool:
        """
        辞書をファイルに保存する
        
        Args:
            file_path: 保存先ファイルのパス
            
        Returns:
            bool: 保存に成功した場合はTrue、そうでない場合はFalse
        """
        pass