# -*- coding: utf-8 -*-
"""
Punctuation Manager for Mojio
Mojio 句読点管理

句読点挿入機能の統合管理クラス
"""

from typing import Optional, List, Dict, Tuple
from .punctuation_interface import PunctuationInterface
from .simple_punctuation import SimplePunctuation


class PunctuationManager:
    """
    句読点挿入機能の統合管理クラス
    
    さまざまな句読点挿入実装を統一的に管理し、
    アプリケーション全体から簡単に利用できるようにする
    """
    
    def __init__(self):
        """句読点管理クラスを初期化"""
        self.simple_punctuation = SimplePunctuation()
        self.current_punctuation: Optional[PunctuationInterface] = None
        self.current_punctuation_type: Optional[str] = None
        self.is_active = False
        
    def initialize_punctuation(self, punctuation_type: str = "simple") -> None:
        """
        句読点挿入機能を初期化する
        
        Args:
            punctuation_type: 句読点挿入タイプ ("simple" など)
        """
        if punctuation_type == "simple":
            self.current_punctuation = self.simple_punctuation
            self.current_punctuation_type = punctuation_type
        else:
            raise ValueError(f"サポートされていない句読点挿入タイプ: {punctuation_type}")
            
        self.is_active = True
        
    def insert_punctuation(self, text: str) -> str:
        """
        テキストに句読点を挿入する
        
        Args:
            text: 句読点を挿入するテキスト
            
        Returns:
            str: 句読点が挿入されたテキスト
        """
        if not self.is_active or self.current_punctuation is None:
            return text
            
        return self.current_punctuation.insert_punctuation(text)
    
    def analyze_context(self, text: str) -> List[Dict[str, any]]:
        """
        テキストの文脈を分析する
        
        Args:
            text: 分析対象のテキスト
            
        Returns:
            List[Dict[str, any]]: 文脈分析結果のリスト
        """
        if not self.is_active or self.current_punctuation is None:
            return []
            
        return self.current_punctuation.analyze_context(text)
    
    def get_punctuation_positions(self, text: str) -> List[Tuple[int, str]]:
        """
        句読点を挿入する位置を取得する
        
        Args:
            text: 分析対象のテキスト
            
        Returns:
            List[Tuple[int, str]]: 句読点を挿入する位置と種類のリスト
        """
        if not self.is_active or self.current_punctuation is None:
            return []
            
        return self.current_punctuation.get_punctuation_positions(text)
    
    def is_punctuation_initialized(self) -> bool:
        """
        句読点挿入機能が初期化されているかを返す
        
        Returns:
            bool: 初期化済みならTrue
        """
        if self.current_punctuation is None:
            return False
        return True
    
    def switch_punctuation(self, punctuation_type: str) -> None:
        """
        句読点挿入機能を切り替える
        
        Args:
            punctuation_type: 句読点挿入タイプ ("simple" など)
        """
        # 現在アクティブな場合は停止
        self.is_active = False
        
        # 句読点挿入機能を切り替え
        self.initialize_punctuation(punctuation_type)