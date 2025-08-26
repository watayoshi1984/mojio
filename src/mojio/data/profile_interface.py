# -*- coding: utf-8 -*-
"""
Profile Interface for Mojio
Mojio プロファイルインターフェース

プロファイル管理の抽象インターフェース定義
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class ProfileInterface(ABC):
    """
    プロファイル管理の抽象インターフェース
    
    さまざまなプロファイル管理実装を統一的に扱うためのインターフェース
    """
    
    @abstractmethod
    def create_profile(self, name: str, settings: Dict[str, any]) -> bool:
        """
        プロファイルを作成する
        
        Args:
            name: プロファイル名
            settings: 設定情報
            
        Returns:
            bool: 作成に成功した場合はTrue、そうでない場合はFalse
        """
        pass
    
    @abstractmethod
    def update_profile(self, profile_id: int, name: Optional[str] = None, settings: Optional[Dict[str, any]] = None) -> bool:
        """
        プロファイルを更新する
        
        Args:
            profile_id: プロファイルID
            name: 新しいプロファイル名（オプション）
            settings: 新しい設定情報（オプション）
            
        Returns:
            bool: 更新に成功した場合はTrue、そうでない場合はFalse
        """
        pass
    
    @abstractmethod
    def delete_profile(self, profile_id: int) -> bool:
        """
        プロファイルを削除する
        
        Args:
            profile_id: プロファイルID
            
        Returns:
            bool: 削除に成功した場合はTrue、そうでない場合はFalse
        """
        pass
    
    @abstractmethod
    def list_profiles(self) -> List[Dict[str, any]]:
        """
        プロファイル一覧を取得する
        
        Returns:
            List[Dict[str, any]]: プロファイル情報のリスト
        """
        pass
    
    @abstractmethod
    def get_profile(self, profile_id: int) -> Optional[Dict[str, any]]:
        """
        IDでプロファイルを取得する
        
        Args:
            profile_id: プロファイルID
            
        Returns:
            Optional[Dict[str, any]]: プロファイル情報（見つからない場合はNone）
        """
        pass
    
    @abstractmethod
    def get_profile_by_name(self, name: str) -> Optional[Dict[str, any]]:
        """
        名前でプロファイルを取得する
        
        Args:
            name: プロファイル名
            
        Returns:
            Optional[Dict[str, any]]: プロファイル情報（見つからない場合はNone）
        """
        pass