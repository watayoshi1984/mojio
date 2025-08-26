# -*- coding: utf-8 -*-
"""
Keyword Highlight Interface
キーワードハイライトの抽象インターフェース

さまざまなキーワードハイライト実装を統一的に扱うためのインターフェース
"""

from abc import ABC, abstractmethod
from typing import List
from PySide6.QtWidgets import QTextEdit


class KeywordHighlightInterface(ABC):
    """
    キーワードハイライトの抽象インターフェース
    
    さまざまなキーワードハイライト実装を統一的に扱うためのインターフェース
    """
    
    @abstractmethod
    def set_keywords(self, keywords: List[str]) -> None:
        """
        ハイライトするキーワードを設定する
        
        Args:
            keywords: ハイライトするキーワードのリスト
        """
        pass
    
    @abstractmethod
    def add_keyword(self, keyword: str) -> None:
        """
        ハイライトするキーワードを追加する
        
        Args:
            keyword: 追加するキーワード
        """
        pass
    
    @abstractmethod
    def remove_keyword(self, keyword: str) -> None:
        """
        ハイライトするキーワードを削除する
        
        Args:
            keyword: 削除するキーワード
        """
        pass
    
    @abstractmethod
    def highlight_text(self, text_edit: QTextEdit) -> None:
        """
        QTextEdit内のテキストにキーワードをハイライト表示する
        
        Args:
            text_edit: ハイライト表示するQTextEditウィジェット
        """
        pass