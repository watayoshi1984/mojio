# -*- coding: utf-8 -*-
"""
Global Shortcut Interface for Mojio
Mojio グローバルショートカットインターフェース

グローバルショートカット機能の抽象インターフェース定義
"""

from abc import ABC, abstractmethod
from typing import Callable


class GlobalShortcutInterface(ABC):
    """
    グローバルショートカット機能の抽象インターフェース
    
    さまざまなグローバルショートカット実装を統一的に扱うためのインターフェース
    """
    
    @abstractmethod
    def register_shortcut(self, shortcut: str, callback: Callable[[], None]) -> None:
        """
        グローバルショートカットを登録する
        
        Args:
            shortcut: ショートカットキーの組み合わせ (例: "ctrl+shift+space")
            callback: ショートカットが押されたときに呼び出されるコールバック関数
        """
        pass
    
    @abstractmethod
    def unregister_shortcut(self, shortcut: str) -> None:
        """
        グローバルショートカットの登録を解除する
        
        Args:
            shortcut: 登録を解除するショートカットキーの組み合わせ
        """
        pass
    
    @abstractmethod
    def start_listening(self) -> None:
        """
        グローバルショートカットの監視を開始する
        """
        pass
    
    @abstractmethod
    def stop_listening(self) -> None:
        """
        グローバルショートカットの監視を停止する
        """
        pass