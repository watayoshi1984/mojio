# -*- coding: utf-8 -*-
"""
Settings Dialog Implementation for MOJIO
MOJIO 設定ダイアログ実装

アプリケーションの設定を行うためのダイアログ
"""

import sys
from typing import List

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QListWidget, QListWidgetItem, QCheckBox,
    QSpinBox, QDoubleSpinBox, QGroupBox, QFormLayout
)
from PySide6.QtCore import Qt

from ..data.config_manager import ConfigManager


class SettingsDialog(QDialog):
    """
    MOJIO 設定ダイアログクラス
    
    アプリケーションの設定を行うためのダイアログ
    """
    
    def __init__(self, parent=None):
        """
        設定ダイアログを初期化
        
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
        
        # イベント接続
        self._connect_signals()
        
        # 設定の読み込み
        self._load_settings()
        
    def _setup_window(self) -> None:
        """ウィンドウの基本設定を行う"""
        self.setWindowTitle("設定")
        self.setModal(True)
        self.resize(500, 400)
        
    def _create_widgets(self) -> None:
        """UIウィジェットを作成"""
        # === UI設定グループ ===
        self.ui_group = QGroupBox("UI設定")
        self.ui_layout = QFormLayout()
        
        # ウィンドウ透明度
        self.opacity_label = QLabel("ウィンドウ透明度:")
        self.opacity_spinbox = QDoubleSpinBox()
        self.opacity_spinbox.setRange(0.1, 1.0)
        self.opacity_spinbox.setSingleStep(0.1)
        self.ui_layout.addRow(self.opacity_label, self.opacity_spinbox)
        
        # 最前面表示
        self.always_on_top_checkbox = QCheckBox("常に最前面に表示")
        self.ui_layout.addRow(self.always_on_top_checkbox)
        
        # キーワードハイライト有効化
        self.highlight_enabled_checkbox = QCheckBox("キーワードハイライトを有効化")
        self.ui_layout.addRow(self.highlight_enabled_checkbox)
        
        self.ui_group.setLayout(self.ui_layout)
        
        # === キーワードハイライト設定グループ ===
        self.keyword_group = QGroupBox("キーワードハイライト")
        self.keyword_layout = QVBoxLayout()
        
        # キーワード入力
        self.keyword_input_layout = QHBoxLayout()
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("キーワードを入力してください")
        self.add_keyword_button = QPushButton("追加")
        self.keyword_input_layout.addWidget(self.keyword_input)
        self.keyword_input_layout.addWidget(self.add_keyword_button)
        
        # キーワードリスト
        self.keyword_list = QListWidget()
        
        # キーワード削除ボタン
        self.remove_keyword_button = QPushButton("削除")
        
        self.keyword_layout.addLayout(self.keyword_input_layout)
        self.keyword_layout.addWidget(self.keyword_list)
        self.keyword_layout.addWidget(self.remove_keyword_button)
        
        self.keyword_group.setLayout(self.keyword_layout)
        
        # === 音声認識設定グループ ===
        self.audio_group = QGroupBox("音声認識設定")
        self.audio_layout = QFormLayout()
        
        # VADパラメータ
        self.vad_threshold_label = QLabel("VAD閾値:")
        self.vad_threshold_spinbox = QDoubleSpinBox()
        self.vad_threshold_spinbox.setRange(0.0, 1.0)
        self.vad_threshold_spinbox.setSingleStep(0.05)
        self.audio_layout.addRow(self.vad_threshold_label, self.vad_threshold_spinbox)
        
        self.vad_duration_label = QLabel("VAD最小発話時間 (ms):")
        self.vad_duration_spinbox = QSpinBox()
        self.vad_duration_spinbox.setRange(100, 5000)
        self.vad_duration_spinbox.setSingleStep(100)
        self.audio_layout.addRow(self.vad_duration_label, self.vad_duration_spinbox)
        
        self.audio_group.setLayout(self.audio_layout)
        
        # === ボタン ===
        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("キャンセル")
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        
    def _create_layouts(self) -> None:
        """レイアウトを構築"""
        # メインレイアウト
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.ui_group)
        main_layout.addWidget(self.keyword_group)
        main_layout.addWidget(self.audio_group)
        main_layout.addLayout(self.button_layout)
        
    def _connect_signals(self) -> None:
        """シグナルとスロットを接続"""
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.add_keyword_button.clicked.connect(self._add_keyword)
        self.remove_keyword_button.clicked.connect(self._remove_keyword)
        self.keyword_list.itemSelectionChanged.connect(self._update_remove_button_state)
        
    def _load_settings(self) -> None:
        """設定を読み込む"""
        # UI設定
        ui_config = self.config.get("ui", {}).get("window", {})
        self.opacity_spinbox.setValue(ui_config.get("opacity", 1.0))
        self.always_on_top_checkbox.setChecked(ui_config.get("always_on_top", False))
        self.highlight_enabled_checkbox.setChecked(self.config.get("ui", {}).get("highlight_enabled", True))
        
        # キーワードハイライト設定
        keywords = self.config.get("ui", {}).get("keywords", [])
        self.keyword_list.clear()
        for keyword in keywords:
            item = QListWidgetItem(keyword)
            self.keyword_list.addItem(item)
            
        # 音声認識設定
        audio_config = self.config.get("audio", {})
        vad_config = audio_config.get("vad", {})
        self.vad_threshold_spinbox.setValue(vad_config.get("threshold", 0.5))
        self.vad_duration_spinbox.setValue(vad_config.get("min_speech_duration", 500))
        
    def _save_settings(self) -> None:
        """設定を保存する"""
        # UI設定
        ui_config = self.config.setdefault("ui", {}).setdefault("window", {})
        ui_config["opacity"] = self.opacity_spinbox.value()
        ui_config["always_on_top"] = self.always_on_top_checkbox.isChecked()
        self.config["ui"]["highlight_enabled"] = self.highlight_enabled_checkbox.isChecked()
        
        # キーワードハイライト設定
        keywords = []
        for i in range(self.keyword_list.count()):
            item = self.keyword_list.item(i)
            keywords.append(item.text())
        self.config["ui"]["keywords"] = keywords
        
        # 音声認識設定
        audio_config = self.config.setdefault("audio", {})
        vad_config = audio_config.setdefault("vad", {})
        vad_config["threshold"] = self.vad_threshold_spinbox.value()
        vad_config["min_speech_duration"] = self.vad_duration_spinbox.value()
        
        # 設定を保存
        self.config_manager.save_config()
        
    def _add_keyword(self) -> None:
        """キーワードを追加"""
        keyword = self.keyword_input.text().strip()
        if keyword and not self._keyword_exists(keyword):
            item = QListWidgetItem(keyword)
            self.keyword_list.addItem(item)
            self.keyword_input.clear()
            
    def _remove_keyword(self) -> None:
        """選択されたキーワードを削除"""
        selected_items = self.keyword_list.selectedItems()
        if selected_items:
            for item in selected_items:
                self.keyword_list.takeItem(self.keyword_list.row(item))
                
    def _keyword_exists(self, keyword: str) -> bool:
        """キーワードが既に存在するかチェック"""
        for i in range(self.keyword_list.count()):
            item = self.keyword_list.item(i)
            if item.text() == keyword:
                return True
        return False
        
    def _update_remove_button_state(self) -> None:
        """削除ボタンの状態を更新"""
        has_selection = len(self.keyword_list.selectedItems()) > 0
        self.remove_keyword_button.setEnabled(has_selection)
        
    def accept(self) -> None:
        """OKボタンがクリックされたときの処理"""
        self._save_settings()
        super().accept()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = SettingsDialog()
    dialog.show()
    sys.exit(app.exec())