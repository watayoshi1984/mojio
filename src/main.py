#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOJIO Main Entry Point
MOJIO メインエントリーポイント

リアルタイム文字起こしアプリケーションのメイン実行ファイル
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def main():
    """
    アプリケーションのメインエントリーポイント
    """
    try:
        from mojio.gui.main_window import MainWindow
        from PySide6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        app.setApplicationName("MOJIO")
        app.setApplicationVersion("0.1.0")
        
        window = MainWindow()
        window.show()
        
        return app.exec()
        
    except ImportError as e:
        print(f"依存関係が不足しています: {e}")
        print("pip install -r requirements.txt を実行してください")
        return 1
    except Exception as e:
        print(f"アプリケーション実行エラー: {e}")
        return 1

if __name__ == "__main__":
    exit(main())