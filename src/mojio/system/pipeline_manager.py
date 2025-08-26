# -*- coding: utf-8 -*-
"""
Real-time Processing Pipeline Manager for Mojio
Mojio リアルタイム処理パイプライン管理クラス

リアルタイム処理パイプラインの統合管理クラス
"""

from typing import Optional
from .pipeline_interface import RealtimePipelineInterface
from .realtime_pipeline import RealtimeProcessingPipeline


class RealtimePipelineManager:
    """
    リアルタイム処理パイプラインの統合管理クラス
    
    さまざまなリアルタイム処理パイプライン実装を統一的に管理し、
    アプリケーション全体から簡単に利用できるようにする
    """
    
    def __init__(self):
        """リアルタイム処理パイプライン管理クラスを初期化"""
        self.current_pipeline: Optional[RealtimePipelineInterface] = None
        self.current_pipeline_type: Optional[str] = None
        self.is_active = False
        
    def initialize_pipeline(self, pipeline_type: str = "realtime", **kwargs) -> None:
        """
        リアルタイム処理パイプラインを初期化する
        
        Args:
            pipeline_type: パイプラインの種類 ("realtime" など)
            **kwargs: パイプライン初期化パラメータ
        """
        if pipeline_type == "realtime":
            self.current_pipeline = RealtimeProcessingPipeline()
            self.current_pipeline.initialize(**kwargs)
            self.current_pipeline_type = pipeline_type
        else:
            raise ValueError(f"サポートされていないパイプラインタイプ: {pipeline_type}")
            
        self.is_active = True
        
    def start_processing(self) -> None:
        """
        リアルタイム処理パイプラインの処理を開始する
        """
        if not self.is_active or self.current_pipeline is None:
            raise RuntimeError("パイプラインが初期化されていません。initialize_pipeline()を先に呼び出してください。")
            
        self.current_pipeline.start_processing()
        
    def stop_processing(self) -> None:
        """
        リアルタイム処理パイプラインの処理を停止する
        """
        if not self.is_active or self.current_pipeline is None:
            raise RuntimeError("パイプラインが初期化されていません。initialize_pipeline()を先に呼び出してください。")
            
        self.current_pipeline.stop_processing()
        self.is_active = False
        
    def is_processing(self) -> bool:
        """
        リアルタイム処理パイプラインが処理中かどうかを返す
        
        Returns:
            bool: 処理中ならTrue、そうでないならFalse
        """
        if not self.is_active or self.current_pipeline is None:
            return False
        return self.current_pipeline.is_processing()
        
    def set_target_window(self, window_title: Optional[str]) -> None:
        """
        テキスト挿入先のウィンドウを設定する
        
        Args:
            window_title: ウィンドウタイトル（Noneの場合はアクティブウィンドウ）
        """
        if not self.is_active or self.current_pipeline is None:
            raise RuntimeError("パイプラインが初期化されていません。initialize_pipeline()を先に呼び出してください。")
            
        self.current_pipeline.set_target_window(window_title)
        
    def switch_pipeline(self, pipeline_type: str, **kwargs) -> None:
        """
        リアルタイム処理パイプラインを切り替える
        
        Args:
            pipeline_type: パイプラインの種類 ("realtime" など)
            **kwargs: パイプライン初期化パラメータ
        """
        self.initialize_pipeline(pipeline_type, **kwargs)