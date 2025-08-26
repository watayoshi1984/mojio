# -*- coding: utf-8 -*-
"""
Core Features Integration Tests for Mojio
Mojio コア機能統合テスト

コア機能（音声入力、音声認識、テキスト挿入）の統合テスト
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from mojio.audio.audio_manager import AudioInputManager
from mojio.audio.recognition_manager import SpeechRecognitionManager
from mojio.system.text_injection_manager import TextInjectionManager
from mojio.system.realtime_pipeline import RealtimeProcessingPipeline
from mojio.system.pipeline_manager import RealtimePipelineManager


class TestCoreFeaturesIntegration:
    """コア機能統合テスト"""
    
    @patch('mojio.audio.audio_manager.AudioInputManager')
    @patch('mojio.audio.recognition_manager.SpeechRecognitionManager')
    @patch('mojio.system.text_injection_manager.TextInjectionManager')
    def test_audio_to_text_pipeline(self, mock_text_injection_manager, 
                                   mock_recognition_manager, mock_audio_manager):
        """音声からテキストへのパイプラインテスト"""
        # モックの設定
        mock_audio_manager_instance = Mock()
        mock_audio_manager.return_value = mock_audio_manager_instance
        
        mock_recognition_manager_instance = Mock()
        mock_recognition_manager_instance.transcribe.return_value = "テスト音声認識"
        mock_recognition_manager.return_value = mock_recognition_manager_instance
        
        mock_text_injection_manager_instance = Mock()
        mock_text_injection_manager.return_value = mock_text_injection_manager_instance
        
        # パイプラインの初期化
        pipeline = RealtimeProcessingPipeline()
        pipeline.audio_manager = mock_audio_manager_instance
        pipeline.recognition_manager = mock_recognition_manager_instance
        pipeline.text_injection_manager = mock_text_injection_manager_instance
        pipeline.is_active = True
        
        # 録音開始
        pipeline.is_recording = True
        audio_data = np.zeros(16000, dtype=np.float32)
        pipeline.audio_buffer = [audio_data]
        
        # 録音停止（テキスト認識と挿入）
        pipeline._toggle_recording()
        
        # 音声認識が呼び出されたことを確認
        mock_recognition_manager_instance.transcribe.assert_called_once_with(audio_data)
        
        # テキスト挿入が呼び出されたことを確認
        mock_text_injection_manager_instance.inject_text.assert_called_once_with("テスト音声認識", None)
        
        # バッファがクリアされたことを確認
        assert pipeline.audio_buffer == []
        assert pipeline.last_recognized_text == "テスト音声認識"
        
    @patch('mojio.audio.audio_manager.AudioInputManager')
    @patch('mojio.audio.vad_manager.VoiceActivityDetectionManager')
    @patch('mojio.audio.recognition_manager.SpeechRecognitionManager')
    @patch('mojio.system.text_injection_manager.TextInjectionManager')
    def test_audio_to_text_pipeline_with_vad(self, mock_text_injection_manager, 
                                            mock_recognition_manager, mock_vad_manager, 
                                            mock_audio_manager):
        """VADを使用した音声からテキストへのパイプラインテスト"""
        # モックの設定
        mock_audio_manager_instance = Mock()
        mock_audio_manager.return_value = mock_audio_manager_instance
        
        mock_vad_manager_instance = Mock()
        mock_vad_manager_instance.is_speech.return_value = True
        mock_vad_manager.return_value = mock_vad_manager_instance
        
        mock_recognition_manager_instance = Mock()
        mock_recognition_manager_instance.transcribe.return_value = "テスト音声認識"
        mock_recognition_manager.return_value = mock_recognition_manager_instance
        
        mock_text_injection_manager_instance = Mock()
        mock_text_injection_manager.return_value = mock_text_injection_manager_instance
        
        # パイプラインの初期化
        pipeline = RealtimeProcessingPipeline()
        pipeline.audio_manager = mock_audio_manager_instance
        pipeline.vad_manager = mock_vad_manager_instance
        pipeline.recognition_manager = mock_recognition_manager_instance
        pipeline.text_injection_manager = mock_text_injection_manager_instance
        pipeline.is_active = True
        pipeline.vad_enabled = True
        
        # 録音開始
        pipeline.is_recording = True
        audio_data = np.zeros(1024, dtype=np.float32)
        
        # 音声区間の音声データを受信
        pipeline._audio_callback(audio_data)
        assert len(pipeline.audio_buffer) == 1
        
        # 無音区間の音声データを受信（テキスト認識と挿入）
        mock_vad_manager_instance.is_speech.return_value = False
        pipeline._audio_callback(audio_data)
        
        # 音声認識が呼び出されたことを確認
        mock_recognition_manager_instance.transcribe.assert_called_once()
        
        # テキスト挿入が呼び出されたことを確認
        mock_text_injection_manager_instance.inject_text.assert_called_once_with("テスト音声認識", None)
        
        # バッファがクリアされたことを確認
        assert pipeline.audio_buffer == []
        assert pipeline.last_recognized_text == "テスト音声認識"
        
    @patch('mojio.system.realtime_pipeline.RealtimeProcessingPipeline')
    def test_pipeline_manager_integration(self, mock_pipeline_class):
        """パイプラインマネージャの統合テスト"""
        # モックの設定
        mock_pipeline_instance = Mock()
        mock_pipeline_class.return_value = mock_pipeline_instance
        
        # パイプラインマネージャの初期化
        manager = RealtimePipelineManager()
        manager.initialize_pipeline(pipeline_type="realtime")
        
        # 処理開始
        manager.start_processing()
        mock_pipeline_instance.start_processing.assert_called_once()
        
        # 処理停止
        manager.stop_processing()
        mock_pipeline_instance.stop_processing.assert_called_once()
        
        # 処理状態の確認
        mock_pipeline_instance.is_processing.return_value = True
        assert manager.is_processing() is True
        mock_pipeline_instance.is_processing.assert_called_once()
        
    def test_audio_manager_initialization(self):
        """音声入力マネージャの初期化テスト"""
        with patch('mojio.audio.microphone_input.MicrophoneAudioInput') as mock_mic, \
             patch('mojio.audio.loopback_input.LoopbackAudioInput') as mock_loopback:
            
            mock_mic_instance = Mock()
            mock_mic.return_value = mock_mic_instance
            
            mock_loopback_instance = Mock()
            mock_loopback.return_value = mock_loopback_instance
            
            # 音声入力マネージャの初期化
            manager = AudioInputManager()
            manager.initialize()
            
            # マイクとループバック入力が初期化されたことを確認
            mock_mic.assert_called_once()
            mock_loopback.assert_called_once()
            
    def test_speech_recognition_manager_initialization(self):
        """音声認識マネージャの初期化テスト"""
        with patch('mojio.audio.whisper_recognition.WhisperSpeechRecognition') as mock_whisper:
            mock_whisper_instance = Mock()
            mock_whisper.return_value = mock_whisper_instance
            
            # 音声認識マネージャの初期化
            manager = SpeechRecognitionManager()
            manager.initialize_engine(engine_type="whisper", model_size="tiny")
            
            # Whisperエンジンが初期化されたことを確認
            mock_whisper.assert_called_once()
            assert manager.current_engine_type == "whisper"
            assert manager.is_active is True
            
    def test_text_injection_manager_initialization(self):
        """テキスト挿入マネージャの初期化テスト"""
        with patch('mojio.system.pynput_text_injection.PynputTextInjection') as mock_pynput:
            mock_pynput_instance = Mock()
            mock_pynput.return_value = mock_pynput_instance
            
            # テキスト挿入マネージャの初期化
            manager = TextInjectionManager()
            manager.initialize_engine(engine_type="pynput")
            
            # Pynputエンジンが初期化されたことを確認
            mock_pynput.assert_called_once()
            assert manager.current_engine_type == "pynput"
            assert manager.is_active is True


if __name__ == "__main__":
    pytest.main([__file__])