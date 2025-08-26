# -*- coding: utf-8 -*-
"""
Test cases for Dictionary Matching
辞書マッチングのテストケース
"""

import unittest
from src.mojio.data.dictionary_matching import DictionaryMatching


class TestDictionaryMatching(unittest.TestCase):
    """辞書マッチングのテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        self.matcher = DictionaryMatching()
        
    def test_match_text(self):
        """テキストマッチングテスト"""
        text = "今日は良い天気です。良い天気ですね。"
        dictionary = {"良い天気": "晴れ"}
        
        matches = self.matcher.match_text(text, dictionary)
        
        # マッチング結果の検証
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0], ("良い天気", "晴れ", 3, 7))
        self.assertEqual(matches[1], ("良い天気", "晴れ", 10, 14))
        
    def test_replace_text(self):
        """テキスト置換テスト"""
        text = "今日は良い天気です。良い天気ですね。"
        matches = [("良い天気", "晴れ", 3, 7), ("良い天気", "晴れ", 10, 14)]
        
        result = self.matcher.replace_text(text, matches)
        
        # 置換結果の検証
        self.assertEqual(result, "今日は晴れです。晴れですね。")
        
    def test_apply_dictionary(self):
        """辞書適用テスト"""
        text = "今日は良い天気です。良い天気ですね。"
        dictionary = {"良い天気": "晴れ"}
        
        result = self.matcher.apply_dictionary(text, dictionary)
        
        # 辞書適用結果の検証
        self.assertEqual(result, "今日は晴れです。晴れですね。")
        
    def test_match_text_no_matches(self):
        """マッチングなしテスト"""
        text = "今日は雨です。"
        dictionary = {"良い天気": "晴れ"}
        
        matches = self.matcher.match_text(text, dictionary)
        
        # マッチング結果の検証
        self.assertEqual(len(matches), 0)
        
    def test_apply_dictionary_no_matches(self):
        """辞書適用（マッチングなし）テスト"""
        text = "今日は雨です。"
        dictionary = {"良い天気": "晴れ"}
        
        result = self.matcher.apply_dictionary(text, dictionary)
        
        # 辞書適用結果の検証
        self.assertEqual(result, text)
        
    def test_overlapping_matches(self):
        """重複マッチングテスト"""
        text = "ABCAB"
        dictionary = {"ABC": "X", "BCA": "Y"}
        
        matches = self.matcher.match_text(text, dictionary)
        
        # マッチング結果の検証
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0], ("ABC", "X", 0, 3))
        self.assertEqual(matches[1], ("BCA", "Y", 1, 4))


if __name__ == "__main__":
    unittest.main()