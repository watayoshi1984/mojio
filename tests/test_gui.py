# -*- coding: utf-8 -*-
"""
GUI Tests for MOJIO
MOJIO GUI テスト

PySide6 GUIコンポーネントのテスト
"""

import sys
import pytest
from unittest.mock import patch
from pathlib import Path

# プロジェクトパスを追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt

from mojio.gui.main_window import MainWindow
from mojio.data.config_manager import ConfigManager


@pytest.fixture
def qapp():
    """QApplicationフィクスチャ"""
    if not QApplication.instance():
        app = QApplication([])
        yield app
        app.quit()
    else:
        yield QApplication.instance()


@pytest.fixture  
def main_window(qapp):
    """MainWindowフィクスチャ"""
    window = MainWindow()
    yield window
    window.close()


class TestMainWindow:
    """メインウィンドウのテストクラス"""
    
    def test_window_creation(self, main_window):
        """ウィンドウ作成テスト"""
        assert main_window.windowTitle() == "MOJIO - Intelligent Real-time Transcription"
        assert main_window.isVisible() == False  # show()前なので非表示
        
    def test_initial_state(self, main_window):
        """初期状態テスト"""
        assert main_window.is_recording == False
        assert main_window.transcription_text == ""
        assert main_window.record_button.text() == "🎤 録音開始"
        
    def test_button_click(self, main_window):
        """ボタンクリックテスト"""
        # 録音ボタンクリック
        QTest.mouseClick(main_window.record_button, Qt.LeftButton)
        assert main_window.is_recording == True
        assert main_window.record_button.text() == "⏹️ 停止"
        
        # 再度クリックで停止
        QTest.mouseClick(main_window.record_button, Qt.LeftButton)
        assert main_window.is_recording == False
        assert main_window.record_button.text() == "🎤 録音開始"
        
    def test_transcription_update(self, main_window):
        """文字起こし更新テスト"""
        test_text = "これはテストです"
        main_window.update_transcription(test_text)
        
        assert main_window.transcription_text == test_text
        assert main_window.transcription_display.toPlainText() == test_text
        
    def test_audio_level_update(self, main_window):
        """音声レベル更新テスト"""
        # レベル設定（0.0-1.0）
        main_window.set_audio_level(0.5)
        assert main_window.audio_level_bar.value() == 50
        
        main_window.set_audio_level(0.8)
        assert main_window.audio_level_bar.value() == 80


class TestConfigManager:
    """設定管理のテストクラス"""
    
    def test_config_creation(self, tmp_path):
        """設定管理作成テスト"""
        config_manager = ConfigManager(tmp_path)
        assert config_manager.config_dir == tmp_path
        assert isinstance(config_manager.get_config(), dict)
        
    def test_config_get_set(self, tmp_path):
        """設定取得・設定テスト"""
        config_manager = ConfigManager(tmp_path)
        
        # デフォルト値取得
        app_name = config_manager.get("app.name", "Unknown")
        assert app_name in ["MOJIO", "Unknown"]
        
        # 値設定
        config_manager.set("test.value", 123)
        assert config_manager.get("test.value") == 123
        
    def test_config_save_load(self, tmp_path):
        """設定保存・読み込みテスト"""
        config_manager = ConfigManager(tmp_path)
        
        # 値設定・保存
        config_manager.set("test.saved_value", "test_data")
        config_manager.save_config()
        
        # 新しいインスタンスで確認
        new_config_manager = ConfigManager(tmp_path)
        assert new_config_manager.get("test.saved_value") == "test_data"


if __name__ == "__main__":
    pytest.main([__file__])