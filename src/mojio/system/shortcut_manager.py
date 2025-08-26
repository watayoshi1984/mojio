# -*- coding: utf-8 -*-
"""
Global Shortcut Manager for Mojio
Mojio グローバルショートカット管理クラス

グローバルショートカット機能の統合管理クラス
"""

from typing import Callable, Optional
from .shortcut_interface import GlobalShortcutInterface
from .pynput_shortcut import PynputGlobalShortcut


class GlobalShortcutManager:
    """
    グローバルショートカット機能の統合管理クラス
    
    さまざまなグローバルショートカット実装を統一的に管理し、
    アプリケーション全体から簡単に利用できるようにする
    """
    
    def __init__(self):
        """グローバルショートカット管理クラスを初期化"""
        self.current_shortcut: Optional[GlobalShortcutInterface] = None
        self.current_shortcut_type: Optional[str] = None
        self.is_active = False
        
    def initialize_shortcut(self, shortcut_type: str = "pynput") -> None:
        """
        グローバルショートカットエンジンを初期化する
        
        Args:
            shortcut_type: グローバルショートカットエンジンの種類 ("pynput" など)
        """
        if shortcut_type == "pynput":
            self.current_shortcut = PynputGlobalShortcut()
            self.current_shortcut_type = shortcut_type
        else:
            raise ValueError(f"サポートされていないグローバルショートカットエンジンタイプ: {shortcut_type}")
            
        self.is_active = True
        
    def register_shortcut(self, shortcut: str, callback: Callable[[], None]) -> None:
        """
        グローバルショートカットを登録する
        
        Args:
            shortcut: ショートカットキーの組み合わせ (例: "ctrl+shift+space")
            callback: ショートカットが押されたときに呼び出されるコールバック関数
        """
        if not self.is_active or self.current_shortcut is None:
            raise RuntimeError("グローバルショートカットエンジンが初期化されていません。initialize_shortcut()を先に呼び出してください。")
            
        self.current_shortcut.register_shortcut(shortcut, callback)
        
    def unregister_shortcut(self, shortcut: str) -> None:
        """
        グローバルショートカットの登録を解除する
        
        Args:
            shortcut: 登録を解除するショートカットキーの組み合わせ
        """
        if not self.is_active or self.current_shortcut is None:
            raise RuntimeError("グローバルショートカットエンジンが初期化されていません。initialize_shortcut()を先に呼び出してください。")
            
        self.current_shortcut.unregister_shortcut(shortcut)
        
    def start_listening(self) -> None:
        """
        グローバルショートカットの監視を開始する
        """
        if not self.is_active or self.current_shortcut is None:
            raise RuntimeError("グローバルショートカットエンジンが初期化されていません。initialize_shortcut()を先に呼び出してください。")
            
        self.current_shortcut.start_listening()
        
    def stop_listening(self) -> None:
        """
        グローバルショートカットの監視を停止する
        """
        if not self.is_active or self.current_shortcut is None:
            raise RuntimeError("グローバルショートカットエンジンが初期化されていません。initialize_shortcut()を先に呼び出してください。")
            
        self.current_shortcut.stop_listening()
        
    def switch_shortcut(self, shortcut_type: str) -> None:
        """
        グローバルショートカットエンジンを切り替える
        
        Args:
            shortcut_type: グローバルショートカットエンジンの種類 ("pynput" など)
        """
        self.initialize_shortcut(shortcut_type)