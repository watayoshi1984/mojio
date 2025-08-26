# -*- coding: utf-8 -*-
"""
Dictionary Matching Implementation for Mojio
Mojio 辞書マッチング実装

辞書マッチングの具体実装
"""

import re
from typing import List, Dict, Tuple
from .matching_interface import MatchingInterface


class DictionaryMatching(MatchingInterface):
    """
    辞書マッチングの具体実装クラス
    
    テキストと辞書データをマッチングし、
    マッチした部分を置換する機能を提供する
    """
    
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
        matches = []
        
        # 辞書の各エントリについてマッチングを試行
        for word, replacement in dictionary.items():
            # 単語の出現位置をすべて検索
            for match in re.finditer(re.escape(word), text):
                start, end = match.span()
                matches.append((word, replacement, start, end))
                
        # 開始位置順にソート
        matches.sort(key=lambda x: x[2])
        return matches
    
    def replace_text(self, text: str, matches: List[Tuple[str, str, int, int]]) -> str:
        """
        テキスト内のマッチした部分を置換する
        
        Args:
            text: 置換対象のテキスト
            matches: マッチング結果のリスト
            
        Returns:
            str: 置換されたテキスト
        """
        if not matches:
            return text
            
        # 後ろから置換することで位置情報がずれるのを防ぐ
        result = text
        for word, replacement, start, end in reversed(matches):
            result = result[:start] + replacement + result[end:]
            
        return result
    
    def apply_dictionary(self, text: str, dictionary: Dict[str, str]) -> str:
        """
        テキストに辞書を適用する
        
        Args:
            text: 適用対象のテキスト
            dictionary: 辞書データ（キー: 単語、値: 置換語）
            
        Returns:
            str: 辞書適用後のテキスト
        """
        matches = self.match_text(text, dictionary)
        return self.replace_text(text, matches)