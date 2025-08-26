# -*- coding: utf-8 -*-
"""
Simple Punctuation Implementation for Mojio
Mojio 簡易句読点実装

テキストの文脈を分析して句読点を自動的に挿入する
"""

import re
from typing import List, Dict, Tuple
from .punctuation_interface import PunctuationInterface


class SimplePunctuation(PunctuationInterface):
    """
    簡易句読点挿入の具体実装
    
    テキストの文脈を分析して
    句読点を自動的に挿入する機能を提供する
    """
    
    def __init__(self):
        """簡易句読点挿入を初期化"""
        # 句読点を挿入するキーワードパターン
        self.sentence_endings = [
            r'です(?![。、])',
            r'ます(?![。、])',
            r'た(?![。、])',
            r'だ(?![。、])',
            r'である(?![。、])',
            r'だった(?![。、])',
            r'である(?![。、])',
            r'でした(?![。、])',
            r'でしょう(?![。、])',
            r'だろう(?![。、])',
            r'です(?![。、])',
            r'ます(?![。、])',
        ]
        
        # 句読点を挿入する助詞パターン
        self.particle_patterns = [
            r'が(?![。、])',
            r'は(?![。、])',
            r'を(?![。、])',
            r'に(?![。、])',
            r'へ(?![。、])',
            r'と(?![。、])',
            r'から(?![。、])',
            r'より(?![。、])',
            r'で(?![。、])',
        ]
        
        # 並列要素のパターン
        self.parallel_patterns = [
            r'([^、]+)と([^、。]+)(?![、。])',
        ]
        
    def insert_punctuation(self, text: str) -> str:
        """
        テキストに句読点を挿入する
        
        Args:
            text: 句読点を挿入するテキスト
            
        Returns:
            str: 句読点が挿入されたテキスト
        """
        # 既に句読点が末尾にある場合は何もしない
        if text.endswith('。') or text.endswith('、'):
            return text
            
        # 文末に句点を追加
        for pattern in self.sentence_endings:
            text = re.sub(pattern, r'\g<0>。', text)
            
        # 助詞の後に読点を追加
        for pattern in self.particle_patterns:
            text = re.sub(pattern, r'\g<0>、', text)
            
        # 並列要素の間に読点を追加
        for pattern in self.parallel_patterns:
            text = re.sub(pattern, r'\1と、\2', text)
            
        # 末尾に句点を追加（文末表現で終わっていない場合）
        if not re.search(r'[。]$', text) and text:
            text += '。'
            
        return text
    
    def analyze_context(self, text: str) -> List[Dict[str, any]]:
        """
        テキストの文脈を分析する
        
        Args:
            text: 分析対象のテキスト
            
        Returns:
            List[Dict[str, any]]: 文脈分析結果のリスト
        """
        results = []
        
        # 文末表現の検出
        for pattern in self.sentence_endings:
            matches = re.finditer(pattern, text)
            for match in matches:
                results.append({
                    "type": "sentence_ending",
                    "position": match.start(),
                    "text": match.group(),
                    "suggestion": "句点の挿入を検討"
                })
                
        # 助詞の検出
        for pattern in self.particle_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                results.append({
                    "type": "particle",
                    "position": match.start(),
                    "text": match.group(),
                    "suggestion": "読点の挿入を検討"
                })
                
        # 並列要素の検出
        for pattern in self.parallel_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                results.append({
                    "type": "parallel",
                    "position": match.start(),
                    "text": match.group(),
                    "suggestion": "読点の挿入を検討"
                })
                
        return results
    
    def get_punctuation_positions(self, text: str) -> List[Tuple[int, str]]:
        """
        句読点を挿入する位置を取得する
        
        Args:
            text: 分析対象のテキスト
            
        Returns:
            List[Tuple[int, str]]: 句読点を挿入する位置と種類のリスト
                各要素は (位置, 句読点種類) のタプル
        """
        positions = []
        
        # 文末表現の後に句点を挿入する位置
        for pattern in self.sentence_endings:
            matches = re.finditer(pattern, text)
            for match in matches:
                # マッチした位置の後に句点を挿入
                positions.append((match.end(), "。"))
                
        # 助詞の後に読点を挿入する位置
        for pattern in self.particle_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                # マッチした位置の後に読点を挿入
                positions.append((match.end(), "、"))
                
        # 並列要素の間に読点を挿入する位置
        for pattern in self.parallel_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                # 最初の要素と第二の要素の間に読点を挿入
                first_part_end = match.start() + len(match.group(1))
                positions.append((first_part_end, "、"))
                
        # 位置でソート
        positions.sort(key=lambda x: x[0])
        
        return positions