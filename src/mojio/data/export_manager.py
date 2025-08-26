# -*- coding: utf-8 -*-
"""
Export Manager Implementation for Mojio
Mojio エクスポート管理実装

テキスト・字幕ファイルへのエクスポート機能の具体実装
"""

import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from .export_interface import ExportInterface
from .history_manager import HistoryManager


class ExportManager(ExportInterface):
    """
    エクスポート機能の具体実装クラス
    
    テキストファイルとSRT字幕ファイルへの
    データエクスポート機能を提供する
    """
    
    def __init__(self):
        """エクスポート管理を初期化"""
        self.history_manager: Optional[HistoryManager] = None
        
    def initialize(self, history_manager: HistoryManager) -> None:
        """
        エクスポート管理を初期化する
        
        Args:
            history_manager: 履歴管理オブジェクト
        """
        self.history_manager = history_manager
        
    def export_to_text(self, data: List[Dict[str, any]], file_path: str, encoding: str = "utf-8") -> bool:
        """
        テキストファイルにエクスポートする
        
        Args:
            data: エクスポートするデータ
            file_path: 出力ファイルパス
            encoding: ファイルエンコーディング
            
        Returns:
            bool: エクスポートに成功した場合はTrue、そうでない場合はFalse
        """
        try:
            # ファイルのディレクトリが存在しない場合は作成
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            # テキストファイルに書き込み
            with open(file_path, "w", encoding=encoding) as f:
                for entry in data:
                    # タイムスタンプがある場合は含める
                    if "timestamp" in entry:
                        f.write(f"[{entry['timestamp']}] ")
                    # 話者情報がある場合は含める
                    if "speaker" in entry:
                        f.write(f"{entry['speaker']}: ")
                    # テキストを書き込み
                    f.write(f"{entry['text']}\n")
                    
            return True
        except Exception as e:
            print(f"テキストファイルへのエクスポートに失敗しました: {e}")
            return False
            
    def export_to_srt(self, data: List[Dict[str, any]], file_path: str, encoding: str = "utf-8") -> bool:
        """
        SRT字幕ファイルにエクスポートする
        
        Args:
            data: エクスポートするデータ
            file_path: 出力ファイルパス
            encoding: ファイルエンコーディング
            
        Returns:
            bool: エクスポートに成功した場合はTrue、そうでない場合はFalse
        """
        try:
            # ファイルのディレクトリが存在しない場合は作成
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            # SRTファイルに書き込み
            with open(file_path, "w", encoding=encoding) as f:
                for i, entry in enumerate(data, 1):
                    # 字幕番号
                    f.write(f"{i}\n")
                    
                    # タイムスタンプ（仮の時間を作成）
                    start_time = self._format_srt_time(i * 5)  # 5秒間隔で開始時間を作成
                    end_time = self._format_srt_time(i * 5 + 4)  # 4秒間の表示時間
                    f.write(f"{start_time} --> {end_time}\n")
                    
                    # テキストを書き込み
                    f.write(f"{entry['text']}\n")
                    
                    # 空行
                    f.write("\n")
                    
            return True
        except Exception as e:
            print(f"SRTファイルへのエクスポートに失敗しました: {e}")
            return False
            
    def export_history_to_text(self, file_path: str, limit: int = 100, encoding: str = "utf-8") -> bool:
        """
        履歴をテキストファイルにエクスポートする
        
        Args:
            file_path: 出力ファイルパス
            limit: エクスポートするエントリ数の上限
            encoding: ファイルエンコーディング
            
        Returns:
            bool: エクスポートに成功した場合はTrue、そうでない場合はFalse
        """
        if self.history_manager is None:
            raise RuntimeError("履歴管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # 履歴データを取得
            history_data = self.history_manager.list_entries(limit)
            
            # テキストファイルにエクスポート
            return self.export_to_text(history_data, file_path, encoding)
        except Exception as e:
            print(f"履歴のテキストファイルへのエクスポートに失敗しました: {e}")
            return False
            
    def export_history_to_srt(self, file_path: str, limit: int = 100, encoding: str = "utf-8") -> bool:
        """
        履歴をSRT字幕ファイルにエクスポートする
        
        Args:
            file_path: 出力ファイルパス
            limit: エクスポートするエントリ数の上限
            encoding: ファイルエンコーディング
            
        Returns:
            bool: エクスポートに成功した場合はTrue、そうでない場合はFalse
        """
        if self.history_manager is None:
            raise RuntimeError("履歴管理が初期化されていません。initialize()を先に呼び出してください。")
            
        try:
            # 履歴データを取得
            history_data = self.history_manager.list_entries(limit)
            
            # SRTファイルにエクスポート
            return self.export_to_srt(history_data, file_path, encoding)
        except Exception as e:
            print(f"履歴のSRTファイルへのエクスポートに失敗しました: {e}")
            return False
            
    def _format_srt_time(self, seconds: int) -> str:
        """
        秒数をSRT形式のタイムスタンプに変換する
        
        Args:
            seconds: 秒数
            
        Returns:
            str: SRT形式のタイムスタンプ (HH:MM:SS,mmm)
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        milliseconds = 0  # 簡略化のためミリ秒は0とする
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"