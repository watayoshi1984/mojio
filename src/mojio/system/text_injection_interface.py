# -*- coding: utf-8 -*-
"""
Text Injection Interface for Mojio
Mojio テキスト挿入インターフェース

テキスト挿入機能への抽象化インターフェース
"""

from abc import ABC, abstractmethod
from typing import Optional


class TextInjectionInterface(ABC):
    """
    テキスト挿入機能の抽象化インターフェース
    
    各種テキスト挿入方法（クリップボード、直接入力等）の
    共通インターフェースを定義
    """
    
    @abstractmethod
    def inject_text(self, text: str, target_window: Optional[str] = None) -> bool:
        """
        指定されたテキストをアクティブまたは指定されたウィンドウに挿入
        
        Args:
            text: 挿入するテキスト
            target_window: ターゲットウィンドウ名（Noneの場合はアクティブウィンドウ）
            
        Returns:
            bool: 挿入成功ならTrue、失敗ならFalse
        """
        pass
    
    @abstractmethod
    def get_active_window_title(self) -> str:
        """
        現在アクティブなウィンドウのタイトルを取得
        
        Returns:
            str: アクティブウィンドウのタイトル
        """
        pass
    
    @abstractmethod
    def is_text_input_available(self) -> bool:
        """
        現在のウィンドウでテキスト入力が可能かどうかを判定
        
        Returns:
            bool: テキスト入力が可能ならTrue
        """
        pass


# テキスト挿入設定の型定義
TextInjectionConfig = dict[str, int | str | bool]