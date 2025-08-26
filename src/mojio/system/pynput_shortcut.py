# -*- coding: utf-8 -*-
"""
Pynput Global Shortcut Implementation for Mojio
Mojio Pynput グローバルショートカット実装

pynputを使用したグローバルショートカットの具体実装
"""

from typing import Callable, Dict
from pynput import keyboard
from .shortcut_interface import GlobalShortcutInterface


class PynputGlobalShortcut(GlobalShortcutInterface):
    """
    pynputを使用したグローバルショートカット実装
    
    pynputライブラリを使用してグローバルショートカットを監視し、
    ショートカットが押されたときにコールバック関数を呼び出す
    """
    
    def __init__(self):
        """pynputグローバルショートカットを初期化"""
        self.shortcuts: Dict[str, Callable[[], None]] = {}
        self.listener = None
        self.is_listening = False
        self.pressed_keys = set()
        
    def register_shortcut(self, shortcut: str, callback: Callable[[], None]) -> None:
        """
        グローバルショートカットを登録する
        
        Args:
            shortcut: ショートカットキーの組み合わせ (例: "ctrl+shift+space")
            callback: ショートカットが押されたときに呼び出されるコールバック関数
        """
        self.shortcuts[shortcut.lower()] = callback
        
    def unregister_shortcut(self, shortcut: str) -> None:
        """
        グローバルショートカットの登録を解除する
        
        Args:
            shortcut: 登録を解除するショートカットキーの組み合わせ
        """
        shortcut_lower = shortcut.lower()
        if shortcut_lower in self.shortcuts:
            del self.shortcuts[shortcut_lower]
            
    def start_listening(self) -> None:
        """
        グローバルショートカットの監視を開始する
        """
        if self.is_listening:
            return
            
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        self.is_listening = True
        
    def stop_listening(self) -> None:
        """
        グローバルショートカットの監視を停止する
        """
        if not self.is_listening:
            return
            
        if self.listener:
            self.listener.stop()
        self.is_listening = False
        self.pressed_keys.clear()
        
    def _on_press(self, key):
        """
        キーが押されたときの処理
        
        Args:
            key: 押されたキー
        """
        try:
            # 特殊キー（ctrl, shift, altなど）の処理
            if hasattr(key, 'name'):
                self.pressed_keys.add(key.name.lower())
            # 通常キーの処理
            else:
                self.pressed_keys.add(key.char.lower())
        except AttributeError:
            # 特殊キーでchar属性がない場合
            pass
            
        # 現在押されているキーからショートカット文字列を生成
        current_shortcut = '+'.join(sorted(self.pressed_keys))
        
        # 登録されたショートカットと一致するか確認
        if current_shortcut in self.shortcuts:
            self.shortcuts[current_shortcut]()
            
    def _on_release(self, key):
        """
        キーが離されたときの処理
        
        Args:
            key: 離されたキー
        """
        try:
            # 特殊キー（ctrl, shift, altなど）の処理
            if hasattr(key, 'name'):
                self.pressed_keys.discard(key.name.lower())
            # 通常キーの処理
            else:
                self.pressed_keys.discard(key.char.lower())
        except AttributeError:
            # 特殊キーでchar属性がない場合
            pass