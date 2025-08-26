# -*- coding: utf-8 -*-
"""
Speech Recognition Tests for Mojio
Mojio 音声認識テスト

音声認識モジュールのユニットテスト
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from mojio.audio.transcription_interface import SpeechRecognitionInterface
from mojio.audio.whisper_recognition import WhisperSpeechRecognition
from mojio.audio.recognition_manager import SpeechRecognitionManager


class TestSpeechRecognitionInterface:
    """音声認識インターフェースのテスト"""
    
    def test_interface_cannot_be_instantiated(self):
        """抽象クラスはインスタンス化できないことを確認"""
        with pytest.raises(TypeError):
            SpeechRecognitionInterface()


class TestWhisperSpeechRecognition:
    """Whisper音声認識のテスト"""
    
    def test_initialization(self):
        """初期化テスト"""
        with patch('mojio.audio.whisper_recognition.WhisperModel') as mock_model:
            mock_model_instance = Mock()
            mock_model.return_value = mock_model_instance
            
            whisper_recognition = WhisperSpeechRecognition()
            whisper_recognition.initialize(model_size="tiny", device="cpu", compute_type="float32")
            
            # WhisperModelが正しいパラメータで呼び出されたことを確認
            mock_model.assert_called_once_with("tiny", device="cpu", compute_type="float32")
            assert whisper_recognition.is_initialized() is True
    
    def test_transcribe_without_initialization(self):
        """初期化せずに音声認識を実行した場合のエラーテスト"""
        whisper_recognition = WhisperSpeechRecognition()
        
        with pytest.raises(RuntimeError, match="モデルが初期化されていません"):
            whisper_recognition.transcribe(np.zeros(16000, dtype=np.float32))
    
    def test_transcribe_success(self):
        """音声認識成功テスト"""
        with patch('mojio.audio.whisper_recognition.WhisperModel') as mock_model:
            # モックセグメントと情報を作成
            mock_segment = Mock()
            mock_segment.text = "テスト音声認識"
            
            mock_model_instance = Mock()
            mock_model_instance.transcribe.return_value = ([mock_segment], {})
            mock_model.return_value = mock_model_instance
            
            whisper_recognition = WhisperSpeechRecognition()
            whisper_recognition.initialize(model_size="tiny", device="cpu", compute_type="float32")
            
            audio_data = np.zeros(16000, dtype=np.float32)
            result = whisper_recognition.transcribe(audio_data, language="ja")
            
            assert result == "テスト音声認識"
            mock_model_instance.transcribe.assert_called_once_with(audio_data, language="ja", beam_size=5)
    
    def test_get_supported_languages(self):
        """サポート言語取得テスト"""
        whisper_recognition = WhisperSpeechRecognition()
        languages = whisper_recognition.get_supported_languages()
        
        assert isinstance(languages, list)
        assert "ja" in languages
        assert "en" in languages


class TestSpeechRecognitionManager:
    """音声認識管理のテスト"""
    
    def test_initialization(self):
        """初期化テスト"""
        with patch('mojio.audio.whisper_recognition.WhisperModel'):
            manager = SpeechRecognitionManager()
            manager.initialize_engine(engine_type="whisper", model_size="tiny")
            
            assert manager.current_engine_type == "whisper"
            assert manager.is_active is True
    
    def test_transcribe_without_initialization(self):
        """初期化せずに音声認識を実行した場合のエラーテスト"""
        manager = SpeechRecognitionManager()
        
        with pytest.raises(RuntimeError, match="音声認識エンジンが初期化されていません"):
            manager.transcribe(np.zeros(16000, dtype=np.float32))
    
    def test_invalid_engine_type(self):
        """無効なエンジンタイプでの初期化テスト"""
        manager = SpeechRecognitionManager()
        
        with pytest.raises(ValueError, match="サポートされていないエンジンタイプ"):
            manager.initialize_engine(engine_type="invalid_engine")
    
    def test_switch_engine(self):
        """エンジン切り替えテスト"""
        with patch('mojio.audio.whisper_recognition.WhisperModel') as mock_model:
            mock_model_instance = Mock()
            mock_model.return_value = mock_model_instance
            
            manager = SpeechRecognitionManager()
            manager.initialize_engine(engine_type="whisper", model_size="tiny")
            
            # エンジンが正しく初期化されたことを確認
            assert manager.current_engine_type == "whisper"
            assert manager.is_active is True
            
            # 同じエンジンに切り替え
            manager.switch_engine(engine_type="whisper", model_size="base")
            
            # 新しいモデルが初期化されたことを確認
            assert mock_model.call_count == 2


if __name__ == "__main__":
    pytest.main([__file__])