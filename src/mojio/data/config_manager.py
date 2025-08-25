# -*- coding: utf-8 -*-
"""
Configuration Manager for MOJIO
MOJIO 設定管理

PyYAMLを使用した設定ファイルの読み込み・保存
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """
    設定管理クラス
    
    YAML形式の設定ファイルを管理し、
    アプリケーション全体の設定を提供
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        設定管理を初期化
        
        Args:
            config_dir: 設定ディレクトリのパス
        """
        # プロジェクトルートを基準とした設定ディレクトリ
        if config_dir is None:
            project_root = Path(__file__).parent.parent.parent.parent
            self.config_dir = project_root / "config"
        else:
            self.config_dir = config_dir
            
        # 設定ファイルパス
        self.default_config_path = self.config_dir / "default.yaml"
        self.user_config_path = self.config_dir / "user.yaml"
        
        # 設定データ
        self.config: Dict[str, Any] = {}
        
        # 設定ディレクトリ作成
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 設定を読み込み
        self._load_config()
        
    def _load_config(self) -> None:
        """設定ファイルを読み込み"""
        # デフォルト設定を読み込み
        if self.default_config_path.exists():
            try:
                with open(self.default_config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"デフォルト設定読み込みエラー: {e}")
                self.config = {}
        else:
            print(f"デフォルト設定ファイルが見つかりません: {self.default_config_path}")
            self.config = self._get_fallback_config()
            
        # ユーザー設定で上書き
        if self.user_config_path.exists():
            try:
                with open(self.user_config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f) or {}
                    self._merge_config(self.config, user_config)
            except Exception as e:
                print(f"ユーザー設定読み込みエラー: {e}")
                
    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """
        設定辞書をマージ
        
        Args:
            base: ベース設定辞書
            override: 上書き設定辞書
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
                
    def _get_fallback_config(self) -> Dict[str, Any]:
        """
        フォールバック設定を取得
        
        Returns:
            最小限の設定辞書
        """
        return {
            "app": {
                "name": "MOJIO",
                "version": "0.1.0"
            },
            "audio": {
                "input": {
                    "sample_rate": 16000,
                    "channels": 1,
                    "buffer_size": 1024
                }
            },
            "transcription": {
                "model": {
                    "size": "large-v2",
                    "device": "auto"
                },
                "language": {
                    "primary": "ja",
                    "auto_detect": True
                }
            },
            "ui": {
                "window": {
                    "x": 100,
                    "y": 100,
                    "width": 400,
                    "height": 300,
                    "opacity": 1.0,
                    "always_on_top": False
                }
            }
        }
        
    def get_config(self) -> Dict[str, Any]:
        """
        現在の設定を取得
        
        Returns:
            設定辞書
        """
        return self.config
        
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        キーパスで設定値を取得
        
        Args:
            key_path: ドット区切りのキーパス（例: "audio.input.sample_rate"）
            default: デフォルト値
            
        Returns:
            設定値
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
            
    def set(self, key_path: str, value: Any) -> None:
        """
        キーパスで設定値を設定
        
        Args:
            key_path: ドット区切りのキーパス
            value: 設定値
        """
        keys = key_path.split('.')
        config = self.config
        
        # 中間ディクショナリを作成
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
            
        # 最終値を設定
        config[keys[-1]] = value
        
    def save_config(self) -> None:
        """ユーザー設定を保存"""
        try:
            with open(self.user_config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, 
                         default_flow_style=False, 
                         allow_unicode=True,
                         sort_keys=False)
        except Exception as e:
            print(f"設定保存エラー: {e}")
            
    def reset_to_default(self) -> None:
        """設定をデフォルトにリセット"""
        if self.user_config_path.exists():
            self.user_config_path.unlink()
        self._load_config()
        
    def backup_config(self, backup_path: Optional[Path] = None) -> bool:
        """
        設定をバックアップ
        
        Args:
            backup_path: バックアップファイルパス
            
        Returns:
            成功フラグ
        """
        if backup_path is None:
            backup_path = self.config_dir / "backup.yaml"
            
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, 
                         default_flow_style=False, 
                         allow_unicode=True,
                         sort_keys=False)
            return True
        except Exception as e:
            print(f"設定バックアップエラー: {e}")
            return False
            
    def restore_config(self, backup_path: Path) -> bool:
        """
        設定をリストア
        
        Args:
            backup_path: バックアップファイルパス
            
        Returns:
            成功フラグ
        """
        if not backup_path.exists():
            return False
            
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
            self.save_config()
            return True
        except Exception as e:
            print(f"設定リストアエラー: {e}")
            return False