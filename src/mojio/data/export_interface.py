# -*- coding: utf-8 -*-
"""
Export Interface for Mojio
Mojio エクスポートインターフェース

エクスポート機能の抽象インターフェース定義
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class ExportInterface(ABC):
    """
    エクスポート機能の抽象インターフェース
    
    さまざまなエクスポート実装を統一的に扱うためのインターフェース
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass