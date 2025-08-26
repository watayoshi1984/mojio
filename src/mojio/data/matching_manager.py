# -*- coding: utf-8 -*-
"""
Matching Manager for Mojio
Mojio マッチング管理クラス

辞書マッチング機能の統合管理クラス
"""

from typing import List, Dict, Tuple, Optional
from .matching_interface import MatchingInterface
from .dictionary_matching import DictionaryMatching


class MatchingManager:
    """
    辞書マッチング機能の統合管理クラス
    
    さまざまな辞書マッチング実装を統一的に管理し、
    アプリケーション全体から簡単に利用できるようにする
    """
    
    def __init__(self):
        """マッチング管理クラスを初期化"""
        self.current_matching: Optional[MatchingInterface] = None
        self.current_matching_type: Optional[str] = None
        self.is_active = False
        
    def initialize_matching(self, matching_type: str = "dictionary") -> None:
        """
        辞書マッチングを初期化する
        
        Args:
            matching_type: マッチングの種類 ("dictionary" など)
        """
        if matching_type == "dictionary":
            self.current_matching = DictionaryMatching()
            self.current_matching_type = matching_type
        else:
            raise ValueError(f"サポートされていないマッチングタイプ: {matching_type}")
            
        self.is_active = True
        
    def match_text(self, text: str, dictionary: Dict[str, str]) -> List[Tuple[str, str, int, int]]:
        """
        テキストと辞書をマッチングする
        
        Args:
            text: マッチング対象のテキスト
            dictionary: 辞書データ（キー: 単語、値: 置換語）
            
        Returns:
            List[Tuple[str, str, int, int]]: マッチング結果のリスト
        """
        if not self.is_active or self.current_matching is None:
            raise RuntimeError("辞書マッチングが初期化されていません。initialize_matching()を先に呼び出してください。")
            
        return self.current_matching.match_text(text, dictionary)
        
    def replace_text(self, text: str, matches: List[Tuple[str, str, int, int]]) -> str:
        """
        テキスト内のマッチした部分を置換する
        
        Args:
            text: 置換対象のテキスト
            matches: マッチング結果のリスト
            
        Returns:
            str: 置換されたテキスト
        """
        if not self.is_active or self.current_matching is None:
            raise RuntimeError("辞書マッチングが初期化されていません。initialize_matching()を先に呼び出してください。")
            
        return self.current_matching.replace_text(text, matches)
        
    def apply_dictionary(self, text: str, dictionary: Dict[str, str]) -> str:
        """
        テキストに辞書を適用する
        
        Args:
            text: 適用対象のテキスト
            dictionary: 辞書データ（キー: 単語、値: 置換語）
            
        Returns:
            str: 辞書適用後のテキスト
        """
        if not self.is_active or self.current_matching is None:
            raise RuntimeError("辞書マッチングが初期化されていません。initialize_matching()を先に呼び出してください。")
            
        return self.current_matching.apply_dictionary(text, dictionary)
        
    def switch_matching(self, matching_type: str) -> None:
        """
        辞書マッチングを切り替える
        
        Args:
            matching_type: マッチングの種類 ("dictionary" など)
        """
        self.initialize_matching(matching_type)