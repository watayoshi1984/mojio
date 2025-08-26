# -*- coding: utf-8 -*-
"""
History Interface for Mojio
Mojio 履歴インターフェース

履歴管理の抽象インターフェース定義
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class HistoryInterface(ABC):
    """
    履歴管理の抽象インターフェース
    
    さまざまな履歴管理実装を統一的に扱うためのインターフェース
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete_entry(self, entry_id: int) -> bool:
        """
        履歴からエントリを削除する
        
        Args:
            entry_id: エントリID
            
        Returns:
            bool: 削除に成功した場合はTrue、そうでない場合はFalse
        """
        pass
    
    @abstractmethod
    def search_entries(self, keyword: str, limit: int = 100) -> List[Dict[str, any]]:
        """
        履歴からエントリを検索する
        
        Args:
            keyword: 検索キーワード
            limit: 検索結果の上限数
            
        Returns:
            List[Dict[str, any]]: エントリ情報のリスト
        """
        pass
    
    @abstractmethod
    def list_entries(self, limit: int = 100) -> List[Dict[str, any]]:
        """
        履歴のエントリ一覧を取得する
        
        Args:
            limit: 取得するエントリ数の上限
            
        Returns:
            List[Dict[str, any]]: エントリ情報のリスト
        """
        pass
    
    @abstractmethod
    def get_entry(self, entry_id: int) -> Optional[Dict[str, any]]:
        """
        IDでエントリを取得する
        
        Args:
            entry_id: エントリID
            
        Returns:
            Optional[Dict[str, any]]: エントリ情報（見つからない場合はNone）
        """
        pass