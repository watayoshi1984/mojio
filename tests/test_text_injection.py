# -*- coding: utf-8 -*-
"""
Text Injection Tests for Mojio
Mojio テキスト挿入テスト

テキスト挿入モジュールのユニットテスト
"""

import pytest
from unittest.mock import Mock, patch
from mojio.system.text_injection_interface import TextInjectionInterface
from mojio.system.pynput_text_injection import PynputTextInjection
from mojio.system.text_injection_manager import TextInjectionManager


class TestTextInjectionInterface:
    """テキスト挿入インターフェースのテスト"""
    
    def test_interface_cannot_be_instantiated(self):
        """抽象クラスはインスタンス化できないことを確認"""
        with pytest.raises(TypeError):
            TextInjectionInterface()


class TestPynputTextInjection:
    """Pynputテキスト挿入のテスト"""
    
    @patch('mojio.system.pynput_text_injection.Controller')
    @patch('mojio.system.pynput_text_injection.gw')
    def test_inject_text_success(self, mock_gw, mock_controller):
        """テキスト挿入成功テスト"""
        # モックを設定
        mock_controller_instance = Mock()
        mock_controller.return_value = mock_controller_instance
        
        mock_gw.getActiveWindow.return_value = Mock(title="テストウィンドウ")
        
        # テキスト挿入をテスト
        injector = PynputTextInjection()
        result = injector.inject_text("テストメッセージ")
        
        # 結果を検証
        assert result is True
        # 各文字に対してpressとreleaseが呼ばれたことを確認
        assert mock_controller_instance.press.call_count == len("テストメッセージ")
        assert mock_controller_instance.release.call_count == len("テストメッセージ")
    
    @patch('mojio.system.pynput_text_injection.Controller')
    @patch('mojio.system.pynput_text_injection.gw')
    def test_get_active_window_title(self, mock_gw, mock_controller):
        """アクティブウィンドウタイトル取得テスト"""
        # モックを設定
        mock_window = Mock()
        mock_window.title = "アクティブウィンドウ"
        mock_gw.getActiveWindow.return_value = mock_window
        
        # アクティブウィンドウタイトルを取得
        injector = PynputTextInjection()
        title = injector.get_active_window_title()
        
        # 結果を検証
        assert title == "アクティブウィンドウ"
    
    @patch('mojio.system.pynput_text_injection.gw')
    def test_get_active_window_title_none(self, mock_gw):
        """アクティブウィンドウが存在しない場合のテスト"""
        # モックを設定
        mock_gw.getActiveWindow.return_value = None
        
        # アクティブウィンドウタイトルを取得
        injector = PynputTextInjection()
        title = injector.get_active_window_title()
        
        # 結果を検証
        assert title == ""
    
    @patch('mojio.system.pynput_text_injection.Controller')
    @patch('mojio.system.pynput_text_injection.gw')
    def test_is_text_input_available(self, mock_gw, mock_controller):
        """テキスト入力可否判定テスト"""
        # モックを設定
        mock_window = Mock()
        mock_window.title = "テキストエディタ"
        mock_gw.getActiveWindow.return_value = mock_window
        
        # テキスト入力可否を判定
        injector = PynputTextInjection()
        available = injector.is_text_input_available()
        
        # 結果を検証
        assert available is True


class TestTextInjectionManager:
    """テキスト挿入管理のテスト"""
    
    def test_initialization(self):
        """初期化テスト"""
        manager = TextInjectionManager()
        
        assert manager.current_method == "pynput_typing"
        assert manager.is_active is True
    
    @patch('mojio.system.pynput_text_injection.PynputTextInjection.inject_text')
    def test_inject_text(self, mock_inject_text):
        """テキスト挿入テスト"""
        # モックを設定
        mock_inject_text.return_value = True
        
        # テキスト挿入をテスト
        manager = TextInjectionManager()
        result = manager.inject_text("テストメッセージ")
        
        # 結果を検証
        assert result is True
        mock_inject_text.assert_called_once_with("テストメッセージ", None)
    
    def test_switch_method_invalid(self):
        """無効な挿入方法での切り替えテスト"""
        manager = TextInjectionManager()
        
        with pytest.raises(ValueError, match="サポートされていない挿入方法"):
            manager.switch_method("invalid_method")
    
    def test_inject_text_with_method(self):
        """指定された方法でのテキスト挿入テスト"""
        with patch.object(TextInjectionManager, 'switch_method') as mock_switch_method, \
             patch.object(TextInjectionManager, 'inject_text') as mock_inject_text:
            
            mock_inject_text.return_value = True
            
            manager = TextInjectionManager()
            result = manager.inject_text_with_method("テストメッセージ", "pynput_clipboard")
            
            # 結果を検証
            assert result is True
            # 方法の切り替えが正しく行われたことを確認
            assert mock_switch_method.call_count == 2  # 元の方法に戻すための呼び出しも含む


if __name__ == "__main__":
    pytest.main([__file__])