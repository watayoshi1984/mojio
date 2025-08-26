# -*- coding: utf-8 -*-
"""
Test cases for Punctuation
句読点挿入のテストケース
"""

import unittest
from src.mojio.data.simple_punctuation import SimplePunctuation
from src.mojio.data.punctuation_manager import PunctuationManager


class TestSimplePunctuation(unittest.TestCase):
    """簡易句読点挿入のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        self.punctuation = SimplePunctuation()
        
    def test_insert_punctuation(self):
        """句読点挿入テスト"""
        # 句読点が挿入されていないテキスト
        text = "今日は良い天気です明日も良い天気でしょう"
        result = self.punctuation.insert_punctuation(text)
        # 句点が挿入されることを確認
        self.assertIn("。", result)
        
        # 既に句読点が末尾にある場合は何もしない
        text_with_punctuation = "今日は良い天気です。"
        result = self.punctuation.insert_punctuation(text_with_punctuation)
        self.assertEqual(result, text_with_punctuation)
        
    def test_analyze_context(self):
        """文脈分析テスト"""
        # テキストを分析
        text = "今日は良い天気です明日も良い天気でしょう"
        results = self.punctuation.analyze_context(text)
        
        # 分析結果がリストであることを確認
        self.assertIsInstance(results, list)
        
        # 少なくとも1つの分析結果があることを確認
        self.assertGreater(len(results), 0)
        
    def test_get_punctuation_positions(self):
        """句読点挿入位置取得テスト"""
        # テキストの句読点挿入位置を取得
        text = "今日は良い天気です明日も良い天気でしょう"
        positions = self.punctuation.get_punctuation_positions(text)
        
        # 位置情報がリストであることを確認
        self.assertIsInstance(positions, list)
        
        # 少なくとも1つの位置情報があることを確認
        self.assertGreater(len(positions), 0)
        
        # 位置情報の形式を確認
        for position in positions:
            self.assertIsInstance(position, tuple)
            self.assertEqual(len(position), 2)
            self.assertIsInstance(position[0], int)
            self.assertIsInstance(position[1], str)


class TestPunctuationManager(unittest.TestCase):
    """句読点挿入管理のテストクラス"""
    
    def setUp(self):
        """テスト前処理"""
        self.manager = PunctuationManager()
        
    def test_initialize_punctuation(self):
        """句読点挿入初期化テスト"""
        self.manager.initialize_punctuation("simple")
        self.assertTrue(self.manager.is_punctuation_initialized())
        
    def test_insert_punctuation(self):
        """句読点挿入テスト"""
        # 句読点挿入機能を初期化
        self.manager.initialize_punctuation("simple")
        
        # 句読点が挿入されていないテキスト
        text = "今日は良い天気です明日も良い天気でしょう"
        result = self.manager.insert_punctuation(text)
        
        # 句点が挿入されることを確認
        self.assertIn("。", result)
        
    def test_analyze_context(self):
        """文脈分析テスト"""
        # 句読点挿入機能を初期化
        self.manager.initialize_punctuation("simple")
        
        # テキストを分析
        text = "今日は良い天気です明日も良い天気でしょう"
        results = self.manager.analyze_context(text)
        
        # 分析結果がリストであることを確認
        self.assertIsInstance(results, list)
        
    def test_get_punctuation_positions(self):
        """句読点挿入位置取得テスト"""
        # 句読点挿入機能を初期化
        self.manager.initialize_punctuation("simple")
        
        # テキストの句読点挿入位置を取得
        text = "今日は良い天気です明日も良い天気でしょう"
        positions = self.manager.get_punctuation_positions(text)
        
        # 位置情報がリストであることを確認
        self.assertIsInstance(positions, list)


if __name__ == "__main__":
    unittest.main()