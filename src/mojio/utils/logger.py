# -*- coding: utf-8 -*-
"""
Logger for MOJIO
MOJIO用ロガー

アプリケーションのログ記録機能を提供
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class MojioLogger:
    """MOJIOアプリケーションのロガークラス"""
    
    def __init__(self, log_dir: str = "logs", log_level: int = logging.INFO):
        """
        ロガーを初期化する
        
        Args:
            log_dir: ログファイルを保存するディレクトリ
            log_level: ログレベル
        """
        self.log_dir = Path(log_dir)
        self.log_level = log_level
        self.logger = logging.getLogger("mojio")
        self.logger.setLevel(log_level)
        
        # ログディレクトリが存在しない場合は作成
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True, exist_ok=True)
            
        # ファイルハンドラーを設定
        self._setup_file_handler()
        
        # コンソールハンドラーを設定
        self._setup_console_handler()
        
    def _setup_file_handler(self) -> None:
        """ファイルハンドラーを設定する"""
        # 日付ごとのログファイル名
        log_filename = f"mojio_{datetime.now().strftime('%Y%m%d')}.log"
        log_file_path = self.log_dir / log_filename
        
        # ファイルハンドラーを作成
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(self.log_level)
        
        # フォーマッターを設定
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        # ロガーにハンドラーを追加
        self.logger.addHandler(file_handler)
        
    def _setup_console_handler(self) -> None:
        """コンソールハンドラーを設定する"""
        # コンソールハンドラーを作成
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        
        # フォーマッターを設定
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # ロガーにハンドラーを追加
        self.logger.addHandler(console_handler)
        
    def debug(self, message: str) -> None:
        """
        デバッグログを記録する
        
        Args:
            message: ログメッセージ
        """
        self.logger.debug(message)
        
    def info(self, message: str) -> None:
        """
        情報ログを記録する
        
        Args:
            message: ログメッセージ
        """
        self.logger.info(message)
        
    def warning(self, message: str) -> None:
        """
        警告ログを記録する
        
        Args:
            message: ログメッセージ
        """
        self.logger.warning(message)
        
    def error(self, message: str) -> None:
        """
        エラーログを記録する
        
        Args:
            message: ログメッセージ
        """
        self.logger.error(message)
        
    def critical(self, message: str) -> None:
        """
        致命的エラーログを記録する
        
        Args:
            message: ログメッセージ
        """
        self.logger.critical(message)
        
    def exception(self, message: str) -> None:
        """
        例外ログを記録する
        
        Args:
            message: ログメッセージ
        """
        self.logger.exception(message)


# グローバルロガーインスタンス
_logger: Optional[MojioLogger] = None


def get_logger() -> MojioLogger:
    """
    グローバルロガーインスタンスを取得する
    
    Returns:
        MojioLogger: ロガーインスタンス
    """
    global _logger
    if _logger is None:
        _logger = MojioLogger()
    return _logger


def setup_logger(log_dir: str = "logs", log_level: int = logging.INFO) -> MojioLogger:
    """
    ロガーをセットアップする
    
    Args:
        log_dir: ログファイルを保存するディレクトリ
        log_level: ログレベル
        
    Returns:
        MojioLogger: ロガーインスタンス
    """
    global _logger
    _logger = MojioLogger(log_dir, log_level)
    return _logger