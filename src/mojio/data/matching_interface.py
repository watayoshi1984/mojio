# -*- coding: utf-8 -*-
"""
Dictionary Matching Interface for Mojio
Mojio 辞書マッチングインターフェース

辞書マッチングの抽象インターフェース定義
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class MatchingInterface(ABC):
    """
    辞書マッチングの抽象インターフェース
    
    さまざまな辞書マッチング実装を統一的に扱うためのインターフェース
    """
    
    @abstractmethod
    def match_text(self, text: str, dictionary: Dict[str, str]) -> List[Tuple[str, str, int, int]]:
        """
        テキストと辞書をマッチングする
        
        Args:
            text: マッチング対象のテキスト
            dictionary: 辞書データ（キー: 単語、値: 置換語）
            
        Returns:
            List[Tuple[str, str, int, int]]: マッチング結果のリスト
                各要素は (マッチした単語, 置換語, 開始位置, 終了位置) のタプル
        """
        pass
    
    @abstractmethod
    def replace_text(self, text: str, matches: List[Tuple[str, str, int, int]]) -> str:
        """
        テキスト内のマッチした部分を置換する
        
        Args:
            text: 置換対象のテキスト
            matches: マッチング結果のリスト
            
        Returns:
            str: 置換されたテキスト
        """
        pass
    
    @abstractmethod
    def apply_dictionary(self, text: str, dictionary: Dict[str, str]) -> str:
        """
        テキストに辞書を適用する
        
        Args:
            text: 適用対象のテキスト
            dictionary: 辞書データ（キー: 単語、値: 置換語）
            
        Returns:
            str: 辞書適用後のテキスト
        """
        pass