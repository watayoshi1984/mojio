# -*- coding: utf-8 -*-
"""
Audio Input Interface for Mojio
Mojio 音声入力インターフェース

音声入力デバイスへの抽象化インターフェース
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Callable
import numpy as np


class AudioInputInterface(ABC):
    """
    音声入力デバイスの抽象化インターフェース
    
    各種音声入力デバイス（マイク、ループバック等）の
    共通インターフェースを定義
    """
    
    @abstractmethod
    def get_device_list(self) -> List[dict]:
        """
        利用可能な音声入力デバイス一覧を取得
        
        Returns:
            List[dict]: デバイス情報のリスト
                各要素は以下のキーを持つ辞書:
                - 'id': デバイスID
                - 'name': デバイス名
                - 'max_input_channels': 最大入力チャンネル数
                - 'default_samplerate': デフォルトサンプリングレート
        """
        pass
    
    @abstractmethod
    def open_stream(self, 
                   device_id: Optional[int] = None,
                   sample_rate: int = 16000,
                   channels: int = 1,
                   buffer_size: int = 1024) -> None:
        """
        音声ストリームを開く
        
        Args:
            device_id: デバイスID（Noneの場合はデフォルトデバイス）
            sample_rate: サンプリングレート（Hz）
            channels: チャンネル数
            buffer_size: バッファサイズ（フレーム数）
        """
        pass
    
    @abstractmethod
    def close_stream(self) -> None:
        """
        音声ストリームを閉じる
        """
        pass
    
    @abstractmethod
    def start_stream(self, callback: Callable[[np.ndarray], None]) -> None:
        """
        音声ストリームの読み取りを開始
        
        Args:
            callback: 音声データ受信時のコールバック関数
                     引数はnumpy配列（音声データ）
        """
        pass
    
    @abstractmethod
    def stop_stream(self) -> None:
        """
        音声ストリームの読み取りを停止
        """
        pass
    
    @abstractmethod
    def is_stream_active(self) -> bool:
        """
        音声ストリームがアクティブかどうかを返す
        
        Returns:
            bool: ストリームがアクティブならTrue
        """
        pass


# デバイス情報の型定義
AudioDeviceInfo = dict[str, int | str | float]