# -*- coding: utf-8 -*-
"""
Keyword Highlight Implementation
キーワードハイライト機能の実装

テキスト内の特定のキーワードをハイライト表示する機能を提供
"""

import re
from typing import List, Tuple, Dict
from PySide6.QtGui import QTextCharFormat, QColor, QTextCursor
from PySide6.QtWidgets import QTextEdit


class KeywordHighlight:
    """
    キーワードハイライトクラス
    
    テキスト内の特定のキーワードをハイライト表示する機能を提供
    """
    
    def __init__(self):
        """キーワードハイライトを初期化"""
        self.keywords: List[str] = []
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(QColor("#f1c40f"))  # 黄色の背景
        self.highlight_format.setForeground(QColor("#2c3e50"))  # 濃いグレーの文字色
        
    def set_keywords(self, keywords: List[str]) -> None:
        """
        ハイライトするキーワードを設定
        
        Args:
            keywords: ハイライトするキーワードのリスト
        """
        self.keywords = keywords
        
    def add_keyword(self, keyword: str) -> None:
        """
        ハイライトするキーワードを追加
        
        Args:
            keyword: 追加するキーワード
        """
        if keyword not in self.keywords:
            self.keywords.append(keyword)
            
    def remove_keyword(self, keyword: str) -> None:
        """
        ハイライトするキーワードを削除
        
        Args:
            keyword: 削除するキーワード
        """
        if keyword in self.keywords:
            self.keywords.remove(keyword)
            
    def highlight_text(self, text_edit: QTextEdit) -> None:
        """
        QTextEdit内のテキストにキーワードをハイライト表示
        
        Args:
            text_edit: ハイライト表示するQTextEditウィジェット
        """
        # 既存のハイライトをクリア
        cursor = text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()
        
        # 各キーワードをハイライト
        for keyword in self.keywords:
            self._highlight_keyword(text_edit, keyword)
            
    def _highlight_keyword(self, text_edit: QTextEdit, keyword: str) -> None:
        """
        特定のキーワードをハイライト表示
        
        Args:
            text_edit: ハイライト表示するQTextEditウィジェット
            keyword: ハイライトするキーワード
        """
        text = text_edit.toPlainText()
        cursor = text_edit.textCursor()
        
        # キーワードのすべての出現位置を検索
        pattern = re.escape(keyword)
        for match in re.finditer(pattern, text, re.IGNORECASE):
            start, end = match.span()
            
            # カーソルをキーワードの位置に移動
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.KeepAnchor)
            
            # ハイライトフォーマットを適用
            cursor.setCharFormat(self.highlight_format)