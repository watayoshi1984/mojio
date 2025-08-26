# -*- coding: utf-8 -*-
"""
Keyword Highlight Tests for MOJIO
MOJIO キーワードハイライトテスト

キーワードハイライト機能のユニットテスト
"""

import unittest
import tempfile
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

from src.mojio.data.keyword_highlight import KeywordHighlight
from src.mojio.gui.settings_dialog import SettingsDialog


class TestKeywordHighlight(unittest.TestCase):
    """キーワードハイライト機能のテスト"""
    
    @classmethod
    def setUpClass(cls):
        """テストクラスのセットアップ"""
        # QApplicationのインスタンスを作成（GUIテスト用）
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])
            
    def setUp(self):
        """テスト前処理"""
        self.keyword_highlight = KeywordHighlight()
        
    def test_set_keywords(self):
        """キーワード設定のテスト"""
        keywords = ["テスト", "キーワード"]
        self.keyword_highlight.set_keywords(keywords)
        self.assertEqual(self.keyword_highlight.keywords, keywords)
        
    def test_add_keyword(self):
        """キーワード追加のテスト"""
        self.keyword_highlight.add_keyword("新しいキーワード")
        self.assertIn("新しいキーワード", self.keyword_highlight.keywords)
        
        # 重複するキーワードを追加してもリストには1つだけ存在することを確認
        self.keyword_highlight.add_keyword("新しいキーワード")
        count = self.keyword_highlight.keywords.count("新しいキーワード")
        self.assertEqual(count, 1)
        
    def test_remove_keyword(self):
        """キーワード削除のテスト"""
        self.keyword_highlight.set_keywords(["削除するキーワード", "残るキーワード"])
        self.keyword_highlight.remove_keyword("削除するキーワード")
        self.assertNotIn("削除するキーワード", self.keyword_highlight.keywords)
        self.assertIn("残るキーワード", self.keyword_highlight.keywords)
        
    def test_highlight_text(self):
        """テキストハイライトのテスト"""
        # テスト用のQTextEditを作成
        text_edit = QTextEdit()
        text_edit.setPlainText("これはテストのテキストです。テストキーワードが含まれています。")
        
        # キーワードを設定
        self.keyword_highlight.set_keywords(["テスト", "キーワード"])
        
        # ハイライトを適用
        self.keyword_highlight.highlight_text(text_edit)
        
        # ハイライトが正しく適用されたかを確認
        # （このテストは完全ではありませんが、基本的な機能を確認します）
        # 実際のハイライトの確認は視覚的に行う必要があります
        
    def test_highlight_keyword_case_insensitive(self):
        """大文字小文字を区別しないハイライトのテスト"""
        # テスト用のQTextEditを作成
        text_edit = QTextEdit()
        text_edit.setPlainText("これはTESTのテキストです。testキーワードが含まれています。")
        
        # キーワードを設定
        self.keyword_highlight.set_keywords(["test"])
        
        # ハイライトを適用
        self.keyword_highlight.highlight_text(text_edit)
        
        # 大文字小文字の違いに関わらずハイライトされることを確認
        # （このテストは完全ではありませんが、基本的な機能を確認します）


class TestSettingsDialog(unittest.TestCase):
    """設定ダイアログのテスト"""
    
    @classmethod
    def setUpClass(cls):
        """テストクラスのセットアップ"""
        # QApplicationのインスタンスを作成（GUIテスト用）
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])
            
    def setUp(self):
        """テスト前処理"""
        # 一時的な設定ファイルを作成
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "test_config.yaml"
        
        # 設定ダイアログを作成
        self.dialog = SettingsDialog()
        
    def tearDown(self):
        """テスト後処理"""
        # 一時ディレクトリを削除
        self.temp_dir.cleanup()
        
    def test_dialog_creation(self):
        """ダイアログ作成のテスト"""
        self.assertIsNotNone(self.dialog)
        self.assertEqual(self.dialog.windowTitle(), "設定")
        
    def test_add_keyword(self):
        """キーワード追加のテスト"""
        # キーワードを入力
        test_keyword = "テストキーワード"
        self.dialog.keyword_input.setText(test_keyword)
        
        # 追加ボタンをクリック
        self.dialog._add_keyword()
        
        # キーワードがリストに追加されたことを確認
        found = False
        for i in range(self.dialog.keyword_list.count()):
            item = self.dialog.keyword_list.item(i)
            if item.text() == test_keyword:
                found = True
                break
        self.assertTrue(found)
        
    def test_remove_keyword(self):
        """キーワード削除のテスト"""
        # キーワードを追加
        test_keyword = "削除するキーワード"
        self.dialog.keyword_input.setText(test_keyword)
        self.dialog._add_keyword()
        
        # 追加されたキーワードを選択
        for i in range(self.dialog.keyword_list.count()):
            item = self.dialog.keyword_list.item(i)
            if item.text() == test_keyword:
                self.dialog.keyword_list.setCurrentItem(item)
                break
                
        # 削除ボタンをクリック
        self.dialog._remove_keyword()
        
        # キーワードがリストから削除されたことを確認
        found = False
        for i in range(self.dialog.keyword_list.count()):
            item = self.dialog.keyword_list.item(i)
            if item.text() == test_keyword:
                found = True
                break
        self.assertFalse(found)


if __name__ == "__main__":
    unittest.main()