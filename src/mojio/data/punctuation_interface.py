# -*- coding: utf-8 -*-
"""
Punctuation Interface for Mojio
Mojio 句読点インターフェース

句読点挿入の抽象インターフェース定義
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class PunctuationInterface(ABC):
    """
    句読点挿入の抽象インターフェース
    
    さまざまな句読点挿入実装を統一的に扱うためのインターフェース
    """
    
    @abstractmethod
    def insert_punctuation(self, text: str) -> str:
        """
        テキストに句読点を挿入する
        
        Args:
            text: 句読点を挿入するテキスト
            
        Returns:
            str: 句読点が挿入されたテキスト
        """
        pass
    
    @abstractmethod
    def analyze_context(self, text: str) -> List[Dict[str, any]]:
        """
        テキストの文脈を分析する
        
        Args:
            text: 分析対象のテキスト
            
        Returns:
            List[Dict[str, any]]: 文脈分析結果のリスト
        """
        pass
    
    @abstractmethod
    def get_punctuation_positions(self, text: str) -> List[Tuple[int, str]]:
        """
        句読点を挿入する位置を取得する
        
        Args:
            text: 分析対象のテキスト
            
        Returns:
            List[Tuple[int, str]]: 句読点を挿入する位置と種類のリスト
                各要素は (位置, 句読点種類) のタプル
        """
        pass