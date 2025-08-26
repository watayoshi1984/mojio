# -*- coding: utf-8 -*-
"""
Real-time Processing Pipeline Interface for Mojio
Mojio リアルタイム処理パイプラインインターフェース

リアルタイム処理パイプラインの抽象インターフェース定義
"""

from abc import ABC, abstractmethod
from typing import Optional


class RealtimePipelineInterface(ABC):
    """
    リアルタイム処理パイプラインの抽象インターフェース
    
    音声入力、音声認識、テキスト挿入を統合した
    リアルタイム処理パイプラインの共通インターフェース
    """
    
    @abstractmethod
    def initialize(self, 
                  input_type: str = "microphone",
                  vad_enabled: bool = True,
                  shortcut_enabled: bool = True) -> None:
        """
        リアルタイム処理パイプラインを初期化する
        
        Args:
            input_type: 音声入力タイプ ("microphone" または "loopback")
            vad_enabled: 音声区間検出を有効にするかどうか
            shortcut_enabled: グローバルショートカットを有効にするかどうか
        """
        pass
    
    @abstractmethod
    def start_processing(self) -> None:
        """
        リアルタイム処理パイプラインの処理を開始する
        """
        pass
    
    @abstractmethod
    def stop_processing(self) -> None:
        """
        リアルタイム処理パイプラインの処理を停止する
        """
        pass
    
    @abstractmethod
    def is_processing(self) -> bool:
        """
        リアルタイム処理パイプラインが処理中かどうかを返す
        
        Returns:
            bool: 処理中ならTrue、そうでないならFalse
        """
        pass
    
    @abstractmethod
    def set_target_window(self, window_title: Optional[str]) -> None:
        """
        テキスト挿入先のウィンドウを設定する
        
        Args:
            window_title: ウィンドウタイトル（Noneの場合はアクティブウィンドウ）
        """
        pass