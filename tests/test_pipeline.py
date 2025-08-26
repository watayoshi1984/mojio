# -*- coding: utf-8 -*-
"""
Real-time Processing Pipeline Tests for Mojio
Mojio リアルタイム処理パイプラインテスト

リアルタイム処理パイプラインのユニットテスト
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from mojio.system.pipeline_interface import RealtimePipelineInterface
from mojio.system.realtime_pipeline import RealtimeProcessingPipeline
from mojio.system.pipeline_manager import RealtimePipelineManager


class TestRealtimePipelineInterface:
    """リアルタイム処理パイプラインインターフェースのテスト"""
    
    def test_interface_cannot_be_instantiated(self):
        """抽象クラスはインスタンス化できないことを確認"""
        with pytest.raises(TypeError):
            RealtimePipelineInterface()


class TestRealtimeProcessingPipeline:
    """リアルタイム処理パイプラインのテスト"""
    
    def test_initialization(self):
        """初期化テスト"""
        pipeline = RealtimeProcessingPipeline()
        
        assert pipeline.input_type == "microphone"
        assert pipeline.vad_enabled is True
        assert pipeline.shortcut_enabled is True
        assert pipeline.target_window is None
        assert pipeline.is_active is False
        assert pipeline.is_recording is False
        assert pipeline.audio_buffer == []
        assert pipeline.last_recognized_text == ""
        assert pipeline.shortcut_key == "ctrl+shift+space"
        
    @patch('mojio.audio.audio_manager.AudioInputManager')
    @patch('mojio.audio.vad_manager.VoiceActivityDetectionManager')
    @patch('mojio.audio.recognition_manager.SpeechRecognitionManager')
    @patch('mojio.system.text_injection_manager.TextInjectionManager')
    @patch('mojio.system.shortcut_manager.GlobalShortcutManager')
    def test_initialize(self, mock_shortcut_manager, mock_text_injection_manager, 
                       mock_recognition_manager, mock_vad_manager, mock_audio_manager):
        """初期化テスト"""
        pipeline = RealtimeProcessingPipeline()
        pipeline.initialize(
            input_type="loopback",
            vad_enabled=False,
            shortcut_enabled=False
        )
        
        assert pipeline.input_type == "loopback"
        assert pipeline.vad_enabled is False
        assert pipeline.shortcut_enabled is False
        assert pipeline.is_active is True
        
    def test_start_processing_without_initialization(self):
        """初期化せずに処理を開始した場合のエラーテスト"""
        pipeline = RealtimeProcessingPipeline()
        
        with pytest.raises(RuntimeError, match="パイプラインが初期化されていません。"):
            pipeline.start_processing()
            
    def test_stop_processing_without_initialization(self):
        """初期化せずに処理を停止した場合のテスト"""
        pipeline = RealtimeProcessingPipeline()
        # エラーを発生させずに処理が完了することを確認
        pipeline.stop_processing()
        
    def test_is_processing(self):
        """処理中かどうかの判定テスト"""
        pipeline = RealtimeProcessingPipeline()
        assert pipeline.is_processing() is False
        
        # パイプラインを初期化
        with patch('mojio.audio.audio_manager.AudioInputManager'), \
             patch('mojio.audio.vad_manager.VoiceActivityDetectionManager'), \
             patch('mojio.audio.recognition_manager.SpeechRecognitionManager'), \
             patch('mojio.system.text_injection_manager.TextInjectionManager'), \
             patch('mojio.system.shortcut_manager.GlobalShortcutManager'):
            pipeline.initialize()
            assert pipeline.is_processing() is True
            
    def test_set_target_window(self):
        """ターゲットウィンドウ設定テスト"""
        pipeline = RealtimeProcessingPipeline()
        pipeline.set_target_window("テストウィンドウ")
        assert pipeline.target_window == "テストウィンドウ"
        
    @patch('mojio.audio.audio_manager.AudioInputManager')
    @patch('mojio.audio.vad_manager.VoiceActivityDetectionManager')
    @patch('mojio.audio.recognition_manager.SpeechRecognitionManager')
    @patch('mojio.system.text_injection_manager.TextInjectionManager')
    @patch('mojio.system.shortcut_manager.GlobalShortcutManager')
    def test_toggle_recording_start(self, mock_shortcut_manager, mock_text_injection_manager, 
                                   mock_recognition_manager, mock_vad_manager, mock_audio_manager):
        """録音開始テスト"""
        pipeline = RealtimeProcessingPipeline()
        pipeline.initialize()
        
        assert pipeline.is_recording is False
        pipeline._toggle_recording()
        assert pipeline.is_recording is True
        assert pipeline.audio_buffer == []
        
    @patch('mojio.audio.audio_manager.AudioInputManager')
    @patch('mojio.audio.vad_manager.VoiceActivityDetectionManager')
    @patch('mojio.audio.recognition_manager.SpeechRecognitionManager')
    @patch('mojio.system.text_injection_manager.TextInjectionManager')
    @patch('mojio.system.shortcut_manager.GlobalShortcutManager')
    def test_toggle_recording_stop(self, mock_shortcut_manager, mock_text_injection_manager, 
                                  mock_recognition_manager, mock_vad_manager, mock_audio_manager):
        """録音停止テスト"""
        pipeline = RealtimeProcessingPipeline()
        pipeline.initialize()
        
        # 録音開始
        pipeline.is_recording = True
        pipeline.audio_buffer = [np.zeros(16000, dtype=np.float32)]
        
        # モックの設定
        mock_recognition_manager_instance = Mock()
        mock_recognition_manager_instance.transcribe.return_value = "テストテキスト"
        pipeline.recognition_manager = mock_recognition_manager_instance
        
        mock_text_injection_manager_instance = Mock()
        pipeline.text_injection_manager = mock_text_injection_manager_instance
        
        # 録音停止
        pipeline._toggle_recording()
        assert pipeline.is_recording is False
        assert pipeline.audio_buffer == []
        assert pipeline.last_recognized_text == "テストテキスト"
        
        # 音声認識とテキスト挿入が呼び出されたことを確認
        mock_recognition_manager_instance.transcribe.assert_called_once()
        mock_text_injection_manager_instance.inject_text.assert_called_once_with("テストテキスト", None)
        
    def test_audio_callback_when_not_recording(self):
        """録音中でない場合の音声コールバックテスト"""
        pipeline = RealtimeProcessingPipeline()
        audio_data = np.zeros(1024, dtype=np.float32)
        
        # 録音中でない場合は何も処理されないことを確認
        pipeline._audio_callback(audio_data)
        assert pipeline.audio_buffer == []
        
    @patch('mojio.audio.vad_manager.VoiceActivityDetectionManager')
    def test_audio_callback_with_vad_speech(self, mock_vad_manager):
        """VAD有効時で音声がある場合の音声コールバックテスト"""
        pipeline = RealtimeProcessingPipeline()
        pipeline.is_recording = True
        pipeline.vad_enabled = True
        
        audio_data = np.zeros(1024, dtype=np.float32)
        
        # VADが音声を検出したと仮定
        mock_vad_manager_instance = Mock()
        mock_vad_manager_instance.is_speech.return_value = True
        pipeline.vad_manager = mock_vad_manager_instance
        
        pipeline._audio_callback(audio_data)
        assert len(pipeline.audio_buffer) == 1
        assert pipeline.audio_buffer[0] is audio_data
        
    @patch('mojio.audio.vad_manager.VoiceActivityDetectionManager')
    @patch('mojio.audio.recognition_manager.SpeechRecognitionManager')
    @patch('mojio.system.text_injection_manager.TextInjectionManager')
    def test_audio_callback_with_vad_silence(self, mock_text_injection_manager, 
                                            mock_recognition_manager, mock_vad_manager):
        """VAD有効時で無音の場合の音声コールバックテスト"""
        pipeline = RealtimeProcessingPipeline()
        pipeline.is_recording = True
        pipeline.vad_enabled = True
        pipeline.audio_buffer = [np.zeros(1024, dtype=np.float32)]
        
        audio_data = np.zeros(1024, dtype=np.float32)
        
        # VADが無音を検出したと仮定
        mock_vad_manager_instance = Mock()
        mock_vad_manager_instance.is_speech.return_value = False
        pipeline.vad_manager = mock_vad_manager_instance
        
        # モックの設定
        mock_recognition_manager_instance = Mock()
        mock_recognition_manager_instance.transcribe.return_value = "テストテキスト"
        pipeline.recognition_manager = mock_recognition_manager_instance
        
        mock_text_injection_manager_instance = Mock()
        pipeline.text_injection_manager = mock_text_injection_manager_instance
        
        pipeline._audio_callback(audio_data)
        assert pipeline.audio_buffer == []
        assert pipeline.last_recognized_text == "テストテキスト"
        
        # 音声認識とテキスト挿入が呼び出されたことを確認
        mock_recognition_manager_instance.transcribe.assert_called_once()
        mock_text_injection_manager_instance.inject_text.assert_called_once_with("テストテキスト", None)
        
    def test_audio_callback_without_vad(self):
        """VAD無効時の音声コールバックテスト"""
        pipeline = RealtimeProcessingPipeline()
        pipeline.is_recording = True
        pipeline.vad_enabled = False
        
        audio_data = np.zeros(1024, dtype=np.float32)
        
        pipeline._audio_callback(audio_data)
        assert len(pipeline.audio_buffer) == 1
        assert pipeline.audio_buffer[0] is audio_data


class TestRealtimePipelineManager:
    """リアルタイム処理パイプライン管理のテスト"""
    
    def test_initialization(self):
        """初期化テスト"""
        manager = RealtimePipelineManager()
        
        assert manager.current_pipeline is None
        assert manager.current_pipeline_type is None
        assert manager.is_active is False
        
    def test_initialize_pipeline(self):
        """パイプライン初期化テスト"""
        manager = RealtimePipelineManager()
        manager.initialize_pipeline(pipeline_type="realtime")
        
        assert isinstance(manager.current_pipeline, RealtimeProcessingPipeline)
        assert manager.current_pipeline_type == "realtime"
        assert manager.is_active is True
        
    def test_initialize_pipeline_invalid_type(self):
        """無効なパイプラインタイプでの初期化テスト"""
        manager = RealtimePipelineManager()
        
        with pytest.raises(ValueError, match="サポートされていないパイプラインタイプ"):
            manager.initialize_pipeline(pipeline_type="invalid_type")
            
    def test_start_processing_without_initialization(self):
        """初期化せずに処理を開始した場合のエラーテスト"""
        manager = RealtimePipelineManager()
        
        with pytest.raises(RuntimeError, match="パイプラインが初期化されていません。"):
            manager.start_processing()
            
    def test_stop_processing_without_initialization(self):
        """初期化せずに処理を停止した場合のエラーテスト"""
        manager = RealtimePipelineManager()
        
        with pytest.raises(RuntimeError, match="パイプラインが初期化されていません。"):
            manager.stop_processing()
            
    def test_is_processing_without_initialization(self):
        """初期化せずに処理中かどうかを判定した場合のテスト"""
        manager = RealtimePipelineManager()
        assert manager.is_processing() is False
        
    def test_set_target_window_without_initialization(self):
        """初期化せずにターゲットウィンドウを設定した場合のエラーテスト"""
        manager = RealtimePipelineManager()
        
        with pytest.raises(RuntimeError, match="パイプラインが初期化されていません。"):
            manager.set_target_window("テストウィンドウ")
            
    @patch('mojio.system.realtime_pipeline.RealtimeProcessingPipeline')
    def test_start_processing(self, mock_pipeline_class):
        """処理開始テスト"""
        mock_pipeline_instance = Mock()
        mock_pipeline_class.return_value = mock_pipeline_instance
        
        manager = RealtimePipelineManager()
        manager.initialize_pipeline(pipeline_type="realtime")
        manager.start_processing()
        
        mock_pipeline_instance.start_processing.assert_called_once()
        
    @patch('mojio.system.realtime_pipeline.RealtimeProcessingPipeline')
    def test_stop_processing(self, mock_pipeline_class):
        """処理停止テスト"""
        mock_pipeline_instance = Mock()
        mock_pipeline_class.return_value = mock_pipeline_instance
        
        manager = RealtimePipelineManager()
        manager.initialize_pipeline(pipeline_type="realtime")
        manager.stop_processing()
        
        mock_pipeline_instance.stop_processing.assert_called_once()
        assert manager.is_active is False
        
    @patch('mojio.system.realtime_pipeline.RealtimeProcessingPipeline')
    def test_is_processing(self, mock_pipeline_class):
        """処理中かどうかの判定テスト"""
        mock_pipeline_instance = Mock()
        mock_pipeline_instance.is_processing.return_value = True
        mock_pipeline_class.return_value = mock_pipeline_instance
        
        manager = RealtimePipelineManager()
        manager.initialize_pipeline(pipeline_type="realtime")
        assert manager.is_processing() is True
        
        mock_pipeline_instance.is_processing.assert_called_once()
        
    @patch('mojio.system.realtime_pipeline.RealtimeProcessingPipeline')
    def test_set_target_window(self, mock_pipeline_class):
        """ターゲットウィンドウ設定テスト"""
        mock_pipeline_instance = Mock()
        mock_pipeline_class.return_value = mock_pipeline_instance
        
        manager = RealtimePipelineManager()
        manager.initialize_pipeline(pipeline_type="realtime")
        manager.set_target_window("テストウィンドウ")
        
        mock_pipeline_instance.set_target_window.assert_called_once_with("テストウィンドウ")


if __name__ == "__main__":
    pytest.main([__file__])