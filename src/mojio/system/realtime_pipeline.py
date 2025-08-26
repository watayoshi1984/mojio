# -*- coding: utf-8 -*-
"""
Real-time Processing Pipeline Implementation for Mojio
Mojio リアルタイム処理パイプライン実装

リアルタイム処理パイプラインの具体実装
"""

import numpy as np
import time
import psutil
import gc
from typing import Optional, List, Tuple
from .pipeline_interface import RealtimePipelineInterface
from ..audio.audio_manager import AudioInputManager
from ..audio.vad_manager import VoiceActivityDetectionManager
from ..audio.recognition_manager import SpeechRecognitionManager
from ..audio.speaker_detection_manager import SpeakerDetectionManager
from ..audio.noise_reduction_manager import NoiseReductionManager
from ..system.text_injection_manager import TextInjectionManager
from ..system.shortcut_manager import GlobalShortcutManager
from ..data.dictionary_manager import DictionaryManager
from ..data.matching_manager import MatchingManager
from ..data.punctuation_manager import PunctuationManager
from ..data.history_manager import HistoryManager
from ..data.config_manager import ConfigManager

# Mojio例外とロガーをインポート
from ..exceptions import MojioBaseException, InitializationError, SpeechRecognitionError
from ..utils.logger import get_logger


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
        self.speaker_detection_manager = SpeakerDetectionManager()
        self.noise_reduction_manager = NoiseReductionManager()
        self.text_injection_manager = TextInjectionManager()
        self.shortcut_manager = GlobalShortcutManager()
        self.dictionary_manager = DictionaryManager()
        self.matching_manager = MatchingManager()
        self.punctuation_manager = PunctuationManager()
        self.history_manager = HistoryManager()
        self.config_manager = ConfigManager()
        self.logger = get_logger()
        
        self.input_type = "microphone"
        self.vad_enabled = True
        self.speaker_detection_enabled = False
        self.punctuation_enabled = False
        self.history_enabled = False
        self.shortcut_enabled = True
        self.noise_reduction_enabled = False
        self.target_window: Optional[str] = None
        self.is_active = False
        self.is_recording = False
        self.audio_buffer: List[np.ndarray] = []
        self.last_recognized_text = ""
        
        # パフォーマンスモニタリング
        self.processing_times = []
        self.max_processing_times = 100  # 最大保持数
        self.memory_usage = []
        self.max_memory_usage = 100  # 最大保持数
        
        # メモリ管理設定
        self.max_memory_limit = self.config_manager.get_max_memory_usage()
        self.gc_interval = self.config_manager.get_gc_interval()
        self.last_gc_time = time.time()
        
        # デフォルトのショートカットキー（Ctrl+Shift+Space）
        self.shortcut_key = "ctrl+shift+space"
        
    def initialize(self, 
                  input_type: str = "microphone",
                  vad_enabled: bool = True,
                  speaker_detection_enabled: bool = False,
                  punctuation_enabled: bool = False,
                  history_enabled: bool = False,
                  shortcut_enabled: bool = True,
                  noise_reduction_enabled: bool = False) -> None:
        """
        リアルタイム処理パイプラインを初期化する
        
        Args:
            input_type: 音声入力タイプ ("microphone" または "loopback")
            vad_enabled: 音声区間検出を有効にするかどうか
            speaker_detection_enabled: 話者検出を有効にするかどうか
            punctuation_enabled: 句読点挿入を有効にするかどうか
            history_enabled: 履歴管理を有効にするかどうか
            shortcut_enabled: グローバルショートカットを有効にするかどうか
            noise_reduction_enabled: ノイズ除去を有効にするかどうか
        """
        try:
            self.input_type = input_type
            self.vad_enabled = vad_enabled
            self.speaker_detection_enabled = speaker_detection_enabled
            self.punctuation_enabled = punctuation_enabled
            self.history_enabled = history_enabled
            self.shortcut_enabled = shortcut_enabled
            self.noise_reduction_enabled = noise_reduction_enabled
            
            # 音声入力マネージャを初期化
            self.audio_manager.initialize()
            
            # 音声区間検出マネージャを初期化
            if self.vad_enabled:
                self.vad_manager.initialize_vad(vad_type="silero", sample_rate=16000)
                
            # 話者検出マネージャを初期化
            if self.speaker_detection_enabled:
                self.speaker_detection_manager.initialize_detector(detector_type="simple")
                
            # ノイズ除去マネージャを初期化
            if self.noise_reduction_enabled:
                self.noise_reduction_manager.initialize(algorithm="spectral_gating", sample_rate=16000)
                
            # 音声認識マネージャを初期化
            self.recognition_manager.initialize_engine(engine_type="whisper", model_size="tiny")
            
            # テキスト挿入マネージャを初期化
            self.text_injection_manager.initialize_engine(engine_type="pynput")
            
            # ユーザー辞書マネージャを初期化
            self.dictionary_manager.initialize_dictionary(dictionary_type="user")
            
            # 辞書マッチングマネージャを初期化
            self.matching_manager.initialize_matching(matching_type="dictionary")
            
            # 句読点マネージャを初期化
            if self.punctuation_enabled:
                self.punctuation_manager.initialize_punctuation(punctuation_type="simple")
                
            # 履歴マネージャを初期化
            if self.history_enabled:
                self.history_manager.initialize(database_path="data/mojio.db")
            
            # グローバルショートカットマネージャを初期化
            if self.shortcut_enabled:
                self.shortcut_manager.initialize_shortcut(shortcut_type="pynput")
                self.shortcut_manager.register_shortcut(
                    self.shortcut_key, 
                    self._toggle_recording
                )
                self.shortcut_manager.start_listening()
                
            self.is_active = True
            self.logger.info("リアルタイム処理パイプラインを初期化しました")
        except Exception as e:
            self.logger.error(f"リアルタイム処理パイプラインの初期化中にエラーが発生しました: {e}")
            raise InitializationError(f"リアルタイム処理パイプラインの初期化中にエラーが発生しました: {e}")
            
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
            self.processing_times.clear()  # パフォーマンスデータをクリア
            print("録音を開始しました")
        else:
            # 録音停止
            self.is_recording = False
            # バッファの音声データを結合
            if self.audio_buffer:
                audio_data = np.concatenate(self.audio_buffer)
                # 音声認識を実行
                start_time = time.time()
                recognized_text = self.recognition_manager.transcribe(audio_data)
                processing_time = time.time() - start_time
                self._record_processing_time(processing_time)
                
                # 話者切り替えを検出
                if self.speaker_detection_enabled:
                    speaker_changed = self.speaker_detection_manager.detect_speaker_change(audio_data)
                    if speaker_changed:
                        recognized_text = f"[話者切り替え] {recognized_text}"
                
                # 句読点を挿入
                if self.punctuation_enabled:
                    recognized_text = self.punctuation_manager.insert_punctuation(recognized_text)
                
                # ユーザー辞書から辞書データを取得
                dictionary_entries = self.dictionary_manager.list_entries()
                dictionary = {entry["word"]: entry["reading"] for entry in dictionary_entries if entry["reading"]}
                
                # 辞書マッチングを適用
                if dictionary:
                    matched_text = self.matching_manager.apply_dictionary(recognized_text, dictionary)
                else:
                    matched_text = recognized_text
                
                # 履歴に保存
                if self.history_enabled:
                    self.history_manager.add_entry(matched_text)
                
                # テキストを挿入
                self.text_injection_manager.inject_text(matched_text, self.target_window)
                self.last_recognized_text = matched_text
                print(f"認識結果: {matched_text}")
            self.audio_buffer.clear()
            print("録音を停止しました")
            
    def _audio_callback(self, audio_data: np.ndarray) -> None:
        """
        音声データ受信時のコールバック関数
        
        Args:
            audio_data: 受信した音声データ
        """
        # 録音中でない場合は何もしない
        if not self.is_recording:
            # メモリを解放
            del audio_data
            return
            
        start_time = time.time()
            
        # ノイズ除去が有効な場合
        if self.noise_reduction_enabled:
            try:
                audio_data = self.noise_reduction_manager.reduce_noise(audio_data)
            except Exception as e:
                print(f"ノイズ除去中にエラーが発生しました: {e}")
        
        # 音声区間検出が有効な場合
        if self.vad_enabled:
            # 音声区間を検出
            is_speech = self.vad_manager.is_speech(audio_data)
            
            if is_speech:
                # 音声がある場合はバッファに追加
                self.audio_buffer.append(audio_data.copy())  # コピーを作成
            else:
                # 無音が検出された場合
                if self.audio_buffer:
                    # バッファの音声データを結合して認識
                    buffered_audio = np.concatenate(self.audio_buffer)
                    
                    # 音声認識を実行
                    recognition_start = time.time()
                    recognized_text = self.recognition_manager.transcribe(buffered_audio)
                    processing_time = time.time() - recognition_start
                    self._record_processing_time(processing_time)
                    
                    # 句読点を挿入
                    if self.punctuation_enabled:
                        recognized_text = self.punctuation_manager.insert_punctuation(recognized_text)
                    
                    # ユーザー辞書から辞書データを取得
                    dictionary_entries = self.dictionary_manager.list_entries()
                    dictionary = {entry["word"]: entry["reading"] for entry in dictionary_entries if entry["reading"]}
                    
                    # 辞書マッチングを適用
                    if dictionary:
                        recognized_text = self.matching_manager.apply_dictionary(recognized_text, dictionary)
                    
                    # テキストを挿入
                    self.text_injection_manager.inject_text(recognized_text, self.target_window)
                    
                    # 履歴に保存
                    if self.history_enabled:
                        self.history_manager.add_entry(recognized_text)
                    
                    # 最後に認識したテキストを更新
                    self.last_recognized_text = recognized_text
                    
                    # バッファをクリア
                    self.audio_buffer.clear()
                    
                    # メモリを解放
                    del buffered_audio
        else:
            # VADが無効な場合はすべての音声データをバッファに追加
            self.audio_buffer.append(audio_data.copy())  # コピーを作成
            
        # 処理時間を記録
        total_processing_time = time.time() - start_time
        self._record_processing_time(total_processing_time)
        
        # メモリ使用量を監視
        self._monitor_memory_usage()
        
        # ガベージコレクションを実行
        self._perform_gc()
        
        # 元の音声データを解放
        del audio_data
        
    def _record_processing_time(self, processing_time: float) -> None:
        """
        処理時間を記録する
        
        Args:
            processing_time: 処理時間（秒）
        """
        self.processing_times.append(processing_time)
        # 最大保持数を超えた場合は古いデータを削除
        if len(self.processing_times) > self.max_processing_times:
            self.processing_times.pop(0)
            
    def get_average_processing_time(self) -> float:
        """
        平均処理時間を取得する
        
        Returns:
            float: 平均処理時間（秒）
        """
        if not self.processing_times:
            return 0.0
        return sum(self.processing_times) / len(self.processing_times)
        
    def get_max_processing_time(self) -> float:
        """
        最大処理時間を取得する
        
        Returns:
            float: 最大処理時間（秒）
        """
        if not self.processing_times:
            return 0.0
        return max(self.processing_times)
        
    def _monitor_memory_usage(self) -> None:
        """
        メモリ使用量を監視する
        """
        # 現在のメモリ使用量を取得（MB）
        current_memory = psutil.Process().memory_info().rss / 1024 / 1024
        self.memory_usage.append(current_memory)
        
        # 最大保持数を超えた場合は古いデータを削除
        if len(self.memory_usage) > self.max_memory_usage:
            self.memory_usage.pop(0)
            
        # メモリ使用量が制限を超えている場合、警告を表示
        if self.max_memory_limit > 0 and current_memory > self.max_memory_limit:
            print(f"警告: メモリ使用量が制限を超えています ({current_memory:.2f} MB / {self.max_memory_limit} MB)")
            
    def get_average_memory_usage(self) -> float:
        """
        平均メモリ使用量を取得する
        
        Returns:
            float: 平均メモリ使用量（MB）
        """
        if not self.memory_usage:
            return 0.0
        return sum(self.memory_usage) / len(self.memory_usage)
        
    def get_max_memory_usage(self) -> float:
        """
        最大メモリ使用量を取得する
        
        Returns:
            float: 最大メモリ使用量（MB）
        """
        if not self.memory_usage:
            return 0.0
        return max(self.memory_usage)
        
    def _perform_gc(self) -> None:
        """
        ガベージコレクションを実行する
        """
        current_time = time.time()
        if current_time - self.last_gc_time > self.gc_interval:
            gc.collect()
            self.last_gc_time = current_time
