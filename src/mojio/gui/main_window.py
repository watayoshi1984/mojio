# -*- coding: utf-8 -*-
"""
Main Window Implementation for MOJIO
MOJIO メインウィンドウ実装

PySide6による高機能なユーザーインターフェース
"""

import sys
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLabel, QTextEdit, QProgressBar,
    QStatusBar, QMenuBar, QSystemTrayIcon, QMenu
)
from PySide6.QtCore import Qt, QTimer, Signal as pyqtSignal
from PySide6.QtGui import QIcon, QFont, QPixmap, QAction

from mojio.data.config_manager import ConfigManager


class MainWindow(QMainWindow):
    """
    MOJIO メインウィンドウクラス
    
    アプリケーションのメインGUIを提供し、
    音声認識機能への直感的なアクセスを実現
    """
    
    recording_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        メインウィンドウを初期化
        
        Args:
            parent: 親ウィジェット
        """
        super().__init__(parent)
        
        # 設定管理
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_config()
        
        # ウィンドウの基本設定
        self._setup_window()
        
        # UI コンポーネントの構築
        self._create_widgets()
        self._create_layouts()
        self._create_menu_bar()
        self._create_status_bar()
        self._create_system_tray()
        
        # イベント接続
        self._connect_signals()
        
        # 状態管理
        self.is_recording = False
        self.transcription_text = ""
        
        # タイマー設定
        self._setup_timers()
        
    def _setup_window(self) -> None:
        """ウィンドウの基本設定を行う"""
        # ウィンドウタイトルとアイコン
        self.setWindowTitle("Mojio（もじ夫）- AIで文字起こしを高精度に")
        
        # ウィンドウサイズと位置
        ui_config = self.config.get("ui", {}).get("window", {})
        self.setGeometry(
            ui_config.get("x", 100),
            ui_config.get("y", 100), 
            ui_config.get("width", 400),
            ui_config.get("height", 300)
        )
        
        # 透明度設定
        opacity = ui_config.get("opacity", 1.0)
        self.setWindowOpacity(opacity)
        
        # 最前面表示設定
        if ui_config.get("always_on_top", False):
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            
        # 最小ウィンドウサイズ
        self.setMinimumSize(300, 200)
        
    def _create_widgets(self) -> None:
        """UIウィジェットを作成"""
        # === ヘッダー部分 ===
        self.title_label = QLabel("🎙️ Mojio（もじ夫）")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.status_label = QLabel("準備完了")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                padding: 5px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        
        # === コントロール部分 ===
        self.record_button = QPushButton("🎤 録音開始")
        self.record_button.setMinimumHeight(40)
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        
        self.settings_button = QPushButton("⚙️ 設定")
        self.settings_button.setMinimumHeight(35)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        
        # === 表示部分 ===
        self.transcription_display = QTextEdit()
        self.transcription_display.setPlaceholderText("文字起こし結果がここに表示されます...")
        self.transcription_display.setReadOnly(True)
        self.transcription_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Yu Gothic UI', 'Meiryo UI', sans-serif;
                font-size: 11px;
                line-height: 1.4;
                background-color: #f8f9fa;
            }
        """)
        
        # === プログレスバー ===
        self.audio_level_bar = QProgressBar()
        self.audio_level_bar.setMaximum(100)
        self.audio_level_bar.setValue(0)
        self.audio_level_bar.setTextVisible(False)
        self.audio_level_bar.setMaximumHeight(8)
        self.audio_level_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
                border-radius: 4px;
            }
        """)
        
    def _create_layouts(self) -> None:
        """レイアウトを構築"""
        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # メインレイアウト
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 10, 15, 15)
        
        # ヘッダー部分
        header_layout = QVBoxLayout()
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.status_label)
        header_layout.addWidget(self.audio_level_bar)
        
        # ボタン部分
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.record_button, 3)
        button_layout.addWidget(self.settings_button, 1)
        
        # 全体の構成
        main_layout.addLayout(header_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.transcription_display, 1)
        
    def _create_menu_bar(self) -> None:
        """メニューバーを作成"""
        menubar = self.menuBar()
        
        # ファイルメニュー
        file_menu = menubar.addMenu("ファイル(&F)")
        
        # 履歴表示アクション
        history_action = QAction("履歴表示(&H)", self)
        history_action.setShortcut("Ctrl+H")
        history_action.triggered.connect(self._show_history)
        file_menu.addAction(history_action)
        
        file_menu.addSeparator()
        
        # 終了アクション
        exit_action = QAction("終了(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 設定メニュー
        settings_menu = menubar.addMenu("設定(&S)")
        
        # 設定画面アクション
        config_action = QAction("設定画面(&C)", self)
        config_action.setShortcut("Ctrl+,")
        config_action.triggered.connect(self.settings_requested.emit)
        settings_menu.addAction(config_action)
        
        # ヘルプメニュー
        help_menu = menubar.addMenu("ヘルプ(&H)")
        
        # バージョン情報アクション
        about_action = QAction("バージョン情報(&A)", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
    def _create_status_bar(self) -> None:
        """ステータスバーを作成"""
        self.statusBar().showMessage("準備完了")
        
    def _create_system_tray(self) -> None:
        """システムトレイアイコンを作成"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            
            # トレイメニュー
            tray_menu = QMenu()
            
            show_action = tray_menu.addAction("表示")
            show_action.triggered.connect(self.show)
            
            hide_action = tray_menu.addAction("隠す")
            hide_action.triggered.connect(self.hide)
            
            tray_menu.addSeparator()
            
            quit_action = tray_menu.addAction("終了")
            quit_action.triggered.connect(self.close)
            
            self.tray_icon.setContextMenu(tray_menu)
            
            # アイコンを表示（アイコンファイルがあれば設定）
            self.tray_icon.show()
            
    def _connect_signals(self) -> None:
        """シグナルとスロットを接続"""
        self.record_button.clicked.connect(self._toggle_recording)
        self.settings_button.clicked.connect(self.settings_requested.emit)
        
    def _setup_timers(self) -> None:
        """タイマーを設定"""
        # 音声レベル更新タイマー
        self.audio_timer = QTimer()
        self.audio_timer.timeout.connect(self._update_audio_level)
        
    def _toggle_recording(self) -> None:
        """録音の開始/停止を切り替え"""
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()
            
    def _start_recording(self) -> None:
        """録音を開始"""
        self.is_recording = True
        self.record_button.setText("⏹️ 停止")
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.status_label.setText("🔴 録音中...")
        self.statusBar().showMessage("録音中...")
        
        # 音声レベル更新開始
        self.audio_timer.start(100)
        
        # 録音開始シグナル発信
        self.recording_requested.emit()
        
    def _stop_recording(self) -> None:
        """録音を停止"""
        self.is_recording = False
        self.record_button.setText("🎤 録音開始")
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.status_label.setText("処理中...")
        self.statusBar().showMessage("処理中...")
        
        # 音声レベル更新停止
        self.audio_timer.stop()
        self.audio_level_bar.setValue(0)
        
        # 停止シグナル発信
        self.stop_requested.emit()
        
    def _update_audio_level(self) -> None:
        """音声レベルバーを更新"""
        # 実際の音声レベルは音声処理コンポーネントから取得
        # ここではダミー実装
        import random
        if self.is_recording:
            level = random.randint(10, 80)
            self.audio_level_bar.setValue(level)
            
    def update_transcription(self, text: str) -> None:
        """文字起こし結果を更新"""
        self.transcription_text = text
        self.transcription_display.setText(text)
        
        # 処理完了後のステータス更新
        if not self.is_recording:
            self.status_label.setText("完了")
            self.statusBar().showMessage("準備完了")
            
    def set_audio_level(self, level: float) -> None:
        """音声レベルを設定"""
        # レベル（0.0-1.0）をパーセンテージに変換
        percentage = int(level * 100)
        self.audio_level_bar.setValue(percentage)
        
    def set_window_opacity(self, opacity: float) -> None:
        """
        ウィンドウの透明度を設定する
        
        Args:
            opacity: 透明度 (0.0-1.0)
        """
        # 透明度の範囲を0.0-1.0に制限
        opacity = max(0.0, min(1.0, opacity))
        
        # ウィンドウに透明度を適用
        self.setWindowOpacity(opacity)
        
        # 設定を更新
        self.config.setdefault("ui", {}).setdefault("window", {})["opacity"] = opacity
        
    def set_window_size(self, width: int, height: int) -> None:
        """
        ウィンドウのサイズを設定する
        
        Args:
            width: ウィンドウの幅
            height: ウィンドウの高さ
        """
        # 最小サイズを下回らないように制限
        min_width = self.minimumWidth()
        min_height = self.minimumHeight()
        width = max(min_width, width)
        height = max(min_height, height)
        
        # ウィンドウサイズを変更
        self.resize(width, height)
        
        # 設定を更新
        ui_config = self.config.setdefault("ui", {}).setdefault("window", {})
        ui_config["width"] = width
        ui_config["height"] = height
        
    def save_window_settings(self) -> None:
        """
        現在のウィンドウ設定を保存する
        """
        try:
            ui_config = self.config.setdefault("ui", {}).setdefault("window", {})
            ui_config["x"] = self.x()
            ui_config["y"] = self.y()
            ui_config["width"] = self.width()
            ui_config["height"] = self.height()
            self.config_manager.save_config()
        except Exception as e:
            print(f"ウィンドウ設定保存エラー: {e}")
        
    def _show_history(self) -> None:
        """履歴画面を表示"""
        # TODO: 履歴画面の実装
        self.statusBar().showMessage("履歴機能は準備中です", 2000)
        
    def _show_about(self) -> None:
        """バージョン情報を表示"""
        # TODO: バージョン情報ダイアログの実装
        self.statusBar().showMessage("MOJIO v0.1.0 - Intelligent Real-time Transcription", 3000)
        
    def closeEvent(self, event) -> None:
        """ウィンドウクローズイベント"""
        # 設定を保存
        try:
            ui_config = self.config.setdefault("ui", {}).setdefault("window", {})
            ui_config["x"] = self.x()
            ui_config["y"] = self.y()
            ui_config["width"] = self.width()
            ui_config["height"] = self.height()
            self.config_manager.save_config()
        except Exception as e:
            print(f"設定保存エラー: {e}")
            
        event.accept()
        
        
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())