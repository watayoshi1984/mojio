# -*- coding: utf-8 -*-
"""
Real-time Processing Pipeline Implementation for Mojio
Mojio リアルタイム処理パイプライン実装

リアルタイム処理パイプラインの具体実装
"""

import numpy as np
from typing import Optional, List, Tuple
from .pipeline_interface import RealtimePipelineInterface
from ..audio.audio_manager import AudioInputManager
from ..audio.vad_manager import VoiceActivityDetectionManager
from ..audio.recognition_manager import SpeechRecognitionManager
from ..system.text_injection_manager import TextInjectionManager
from ..system.shortcut_manager import GlobalShortcutManager


class RealtimeProcessingPipeline(RealtimePipelineInterface):
    """
    リアルタイム処理パイプラインの具体実装
    
    音声入力、音声区間検出、音声認識、テキスト挿入を
    統合したリアルタイム処理パイプライン
    """
    
    def __init__(self):
        """リアルタイム処理パイプラインを初期化"""
        self.audio_manager = AudioInputManager()
        self.vad_manager = VoiceActivityDetectionManager()
        self.recognition_manager = SpeechRecognitionManager()
        self.text_injection_manager = TextInjectionManager()
        self.shortcut_manager = GlobalShortcutManager()
        
        self.input_type = "microphone"
        self.vad_enabled = True
        self.shortcut_enabled = True
        self.target_window: Optional[str] = None
        self.is_active = False
        self.is_recording = False
        self.audio_buffer: List[np.ndarray] = []
        self.last_recognized_text = ""
        
        # デフォルトのショートカットキー（Ctrl+Shift+Space）
        self.shortcut_key = "ctrl+shift+space"
        
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
        self.input_type = input_type
        self.vad_enabled = vad_enabled
        self.shortcut_enabled = shortcut_enabled
        
        # 音声入力マネージャを初期化
        self.audio_manager.initialize()
        
        # 音声区間検出マネージャを初期化
        if self.vad_enabled:
            self.vad_manager.initialize_vad(vad_type="silero", sample_rate=16000)
            
        # 音声認識マネージャを初期化
        self.recognition_manager.initialize_engine(engine_type="whisper", model_size="tiny")
        
        # テキスト挿入マネージャを初期化
        self.text_injection_manager.initialize_engine(engine_type="pynput")
        
        # グローバルショートカットマネージャを初期化
        if self.shortcut_enabled:
            self.shortcut_manager.initialize_shortcut(shortcut_type="pynput")
            self.shortcut_manager.register_shortcut(
                self.shortcut_key, 
                self._toggle_recording
            )
            self.shortcut_manager.start_listening()
            
        self.is_active = True
        
    def start_processing(self) -> None:
        """
        リアルタイム処理パイプラインの処理を開始する
        """
        if not self.is_active:
            raise RuntimeError("パイプラインが初期化されていません。initialize()を先に呼び出してください。")
            
        # 音声入力タイプを切り替え
        self.audio_manager.switch_input_type(self.input_type)
        
        # 音声ストリームのコールバックを設定
        self.audio_manager.current_input.start_stream(self._audio_callback)
        
    def stop_processing(self) -> None:
        """
        リアルタイム処理パイプラインの処理を停止する
        """
        if not self.is_active:
            return
            
        # 音声ストリームを停止
        if self.audio_manager.current_input:
            self.audio_manager.current_input.stop_stream()
            
        # グローバルショートカットの監視を停止
        if self.shortcut_enabled:
            self.shortcut_manager.stop_listening()
            
        self.is_active = False
        self.is_recording = False
        self.audio_buffer.clear()
        
    def is_processing(self) -> bool:
        """
        リアルタイム処理パイプラインが処理中かどうかを返す
        
        Returns:
            bool: 処理中ならTrue、そうでないならFalse
        """
        return self.is_active
        
    def set_target_window(self, window_title: Optional[str]) -> None:
        """
        テキスト挿入先のウィンドウを設定する
        
        Args:
            window_title: ウィンドウタイトル（Noneの場合はアクティブウィンドウ）
        """
        self.target_window = window_title
        
    def _toggle_recording(self) -> None:
        """
        録音状態を切り替える（ショートカットコールバック）
        """
        if not self.is_recording:
            # 録音開始
            self.is_recording = True
            self.audio_buffer.clear()
            print("録音を開始しました")
        else:
            # 録音停止
            self.is_recording = False
            # バッファの音声データを結合
            if self.audio_buffer:
                audio_data = np.concatenate(self.audio_buffer)
                # 音声認識を実行
                recognized_text = self.recognition_manager.transcribe(audio_data)
                # テキストを挿入
                self.text_injection_manager.inject_text(recognized_text, self.target_window)
                self.last_recognized_text = recognized_text
                print(f"認識結果: {recognized_text}")
            self.audio_buffer.clear()
            print("録音を停止しました")
            
    def _audio_callback(self, audio_data: np.ndarray) -> None:
        """
        音声データ受信時のコールバック関数
        
        Args:
            audio_data: 音声データ (numpy配列)
        """
        if not self.is_recording:
            return
            
        # 音声区間検出が有効な場合
        if self.vad_enabled:
            # 音声区間かどうかを判定
            if self.vad_manager.is_speech(audio_data):
                # 音声データをバッファに追加
                self.audio_buffer.append(audio_data)
            else:
                # 無音区間の場合はバッファをクリア
                # ただし、最後の認識結果が出ていない場合のみ
                if self.audio_buffer:
                    # バッファの音声データを結合
                    buffered_audio = np.concatenate(self.audio_buffer)
                    # 音声認識を実行
                    recognized_text = self.recognition_manager.transcribe(buffered_audio)
                    # テキストを挿入
                    self.text_injection_manager.inject_text(recognized_text, self.target_window)
                    self.last_recognized_text = recognized_text
                    print(f"認識結果: {recognized_text}")
                    self.audio_buffer.clear()
        else:
            # 音声区間検出が無効な場合はすべての音声データをバッファに追加
            self.audio_buffer.append(audio_data)