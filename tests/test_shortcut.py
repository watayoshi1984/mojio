# -*- coding: utf-8 -*-
"""
Global Shortcut Tests for Mojio
Mojio グローバルショートカットテスト

グローバルショートカットモジュールのユニットテスト
"""

import pytest
from unittest.mock import Mock, patch
from mojio.system.shortcut_interface import GlobalShortcutInterface
from mojio.system.pynput_shortcut import PynputGlobalShortcut
from mojio.system.shortcut_manager import GlobalShortcutManager


class TestGlobalShortcutInterface:
    """グローバルショートカットインターフェースのテスト"""
    
    def test_interface_cannot_be_instantiated(self):
        """抽象クラスはインスタンス化できないことを確認"""
        with pytest.raises(TypeError):
            GlobalShortcutInterface()


class TestPynputGlobalShortcut:
    """Pynputグローバルショートカットのテスト"""
    
    def test_initialization(self):
        """初期化テスト"""
        shortcut = PynputGlobalShortcut()
        
        assert shortcut.shortcuts == {}
        assert shortcut.listener is None
        assert shortcut.is_listening is False
        assert shortcut.pressed_keys == set()
        
    def test_register_shortcut(self):
        """ショートカット登録テスト"""
        shortcut = PynputGlobalShortcut()
        callback = Mock()
        
        shortcut.register_shortcut("ctrl+shift+space", callback)
        
        assert "ctrl+shift+space" in shortcut.shortcuts
        assert shortcut.shortcuts["ctrl+shift+space"] == callback
        
    def test_unregister_shortcut(self):
        """ショートカット登録解除テスト"""
        shortcut = PynputGlobalShortcut()
        callback = Mock()
        
        shortcut.register_shortcut("ctrl+shift+space", callback)
        assert "ctrl+shift+space" in shortcut.shortcuts
        
        shortcut.unregister_shortcut("ctrl+shift+space")
        assert "ctrl+shift+space" not in shortcut.shortcuts
        
    def test_unregister_nonexistent_shortcut(self):
        """存在しないショートカットの登録解除テスト"""
        shortcut = PynputGlobalShortcut()
        
        # エラーを発生させずに処理が完了することを確認
        shortcut.unregister_shortcut("ctrl+shift+space")
        
    @patch('pynput.keyboard.Listener')
    def test_start_listening(self, mock_listener_class):
        """ショートカット監視開始テスト"""
        mock_listener_instance = Mock()
        mock_listener_class.return_value = mock_listener_instance
        
        shortcut = PynputGlobalShortcut()
        shortcut.start_listening()
        
        assert shortcut.is_listening is True
        mock_listener_class.assert_called_once()
        mock_listener_instance.start.assert_called_once()
        
    @patch('pynput.keyboard.Listener')
    def test_stop_listening(self, mock_listener_class):
        """ショートカット監視停止テスト"""
        mock_listener_instance = Mock()
        mock_listener_class.return_value = mock_listener_instance
        
        shortcut = PynputGlobalShortcut()
        shortcut.start_listening()
        assert shortcut.is_listening is True
        
        shortcut.stop_listening()
        assert shortcut.is_listening is False
        assert shortcut.pressed_keys == set()
        mock_listener_instance.stop.assert_called_once()
        
    def test_on_press_with_special_key(self):
        """特殊キー押下時の処理テスト"""
        shortcut = PynputGlobalShortcut()
        callback = Mock()
        shortcut.register_shortcut("ctrl+shift", callback)
        
        # モックキーを作成
        mock_key = Mock()
        mock_key.name = "ctrl"
        
        shortcut._on_press(mock_key)
        assert "ctrl" in shortcut.pressed_keys
        
    def test_on_press_with_character_key(self):
        """文字キー押下時の処理テスト"""
        shortcut = PynputGlobalShortcut()
        callback = Mock()
        shortcut.register_shortcut("a", callback)
        
        # モックキーを作成
        mock_key = Mock()
        mock_key.char = "a"
        
        shortcut._on_press(mock_key)
        assert "a" in shortcut.pressed_keys
        
    def test_on_release_with_special_key(self):
        """特殊キー離したときの処理テスト"""
        shortcut = PynputGlobalShortcut()
        callback = Mock()
        shortcut.register_shortcut("ctrl", callback)
        
        # モックキーを作成
        mock_key = Mock()
        mock_key.name = "ctrl"
        
        shortcut.pressed_keys.add("ctrl")
        shortcut._on_release(mock_key)
        assert "ctrl" not in shortcut.pressed_keys
        
    def test_on_release_with_character_key(self):
        """文字キー離したときの処理テスト"""
        shortcut = PynputGlobalShortcut()
        callback = Mock()
        shortcut.register_shortcut("a", callback)
        
        # モックキーを作成
        mock_key = Mock()
        mock_key.char = "a"
        
        shortcut.pressed_keys.add("a")
        shortcut._on_release(mock_key)
        assert "a" not in shortcut.pressed_keys


class TestGlobalShortcutManager:
    """グローバルショートカット管理のテスト"""
    
    def test_initialization(self):
        """初期化テスト"""
        manager = GlobalShortcutManager()
        
        assert manager.current_shortcut is None
        assert manager.current_shortcut_type is None
        assert manager.is_active is False
        
    def test_initialize_shortcut(self):
        """ショートカット初期化テスト"""
        manager = GlobalShortcutManager()
        manager.initialize_shortcut(shortcut_type="pynput")
        
        assert isinstance(manager.current_shortcut, PynputGlobalShortcut)
        assert manager.current_shortcut_type == "pynput"
        assert manager.is_active is True
        
    def test_initialize_shortcut_invalid_type(self):
        """無効なショートカットタイプでの初期化テスト"""
        manager = GlobalShortcutManager()
        
        with pytest.raises(ValueError, match="サポートされていないグローバルショートカットエンジンタイプ"):
            manager.initialize_shortcut(shortcut_type="invalid_type")
            
    def test_register_shortcut_without_initialization(self):
        """初期化せずにショートカットを登録した場合のエラーテスト"""
        manager = GlobalShortcutManager()
        
        with pytest.raises(RuntimeError, match="グローバルショートカットエンジンが初期化されていません。"):
            manager.register_shortcut("ctrl+shift+space", Mock())
            
    def test_unregister_shortcut_without_initialization(self):
        """初期化せずにショートカットの登録を解除した場合のエラーテスト"""
        manager = GlobalShortcutManager()
        
        with pytest.raises(RuntimeError, match="グローバルショートカットエンジンが初期化されていません。"):
            manager.unregister_shortcut("ctrl+shift+space")
            
    def test_start_listening_without_initialization(self):
        """初期化せずにショートカットの監視を開始した場合のエラーテスト"""
        manager = GlobalShortcutManager()
        
        with pytest.raises(RuntimeError, match="グローバルショートカットエンジンが初期化されていません。"):
            manager.start_listening()
            
    def test_stop_listening_without_initialization(self):
        """初期化せずにショートカットの監視を停止した場合のエラーテスト"""
        manager = GlobalShortcutManager()
        
        with pytest.raises(RuntimeError, match="グローバルショートカットエンジンが初期化されていません。"):
            manager.stop_listening()
            
    @patch('mojio.system.pynput_shortcut.PynputGlobalShortcut')
    def test_register_shortcut(self, mock_shortcut_class):
        """ショートカット登録テスト"""
        mock_shortcut_instance = Mock()
        mock_shortcut_class.return_value = mock_shortcut_instance
        
        manager = GlobalShortcutManager()
        manager.initialize_shortcut(shortcut_type="pynput")
        
        callback = Mock()
        manager.register_shortcut("ctrl+shift+space", callback)
        
        mock_shortcut_instance.register_shortcut.assert_called_once_with("ctrl+shift+space", callback)
        
    @patch('mojio.system.pynput_shortcut.PynputGlobalShortcut')
    def test_unregister_shortcut(self, mock_shortcut_class):
        """ショートカット登録解除テスト"""
        mock_shortcut_instance = Mock()
        mock_shortcut_class.return_value = mock_shortcut_instance
        
        manager = GlobalShortcutManager()
        manager.initialize_shortcut(shortcut_type="pynput")
        
        manager.unregister_shortcut("ctrl+shift+space")
        
        mock_shortcut_instance.unregister_shortcut.assert_called_once_with("ctrl+shift+space")
        
    @patch('mojio.system.pynput_shortcut.PynputGlobalShortcut')
    def test_start_listening(self, mock_shortcut_class):
        """ショートカット監視開始テスト"""
        mock_shortcut_instance = Mock()
        mock_shortcut_class.return_value = mock_shortcut_instance
        
        manager = GlobalShortcutManager()
        manager.initialize_shortcut(shortcut_type="pynput")
        
        manager.start_listening()
        
        mock_shortcut_instance.start_listening.assert_called_once()
        
    @patch('mojio.system.pynput_shortcut.PynputGlobalShortcut')
    def test_stop_listening(self, mock_shortcut_class):
        """ショートカット監視停止テスト"""
        mock_shortcut_instance = Mock()
        mock_shortcut_class.return_value = mock_shortcut_instance
        
        manager = GlobalShortcutManager()
        manager.initialize_shortcut(shortcut_type="pynput")
        
        manager.stop_listening()
        
        mock_shortcut_instance.stop_listening.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])