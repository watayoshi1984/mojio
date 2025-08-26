# -*- coding: utf-8 -*-
"""
Voice Activity Detection Tests for Mojio
Mojio 音声区間検出テスト

音声区間検出モジュールのユニットテスト
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from mojio.audio.vad_interface import VoiceActivityDetectionInterface
from mojio.audio.silero_vad import SileroVoiceActivityDetection
from mojio.audio.vad_manager import VoiceActivityDetectionManager


class TestVoiceActivityDetectionInterface:
    """音声区間検出インターフェースのテスト"""
    
    def test_interface_cannot_be_instantiated(self):
        """抽象クラスはインスタンス化できないことを確認"""
        with pytest.raises(TypeError):
            VoiceActivityDetectionInterface()


class TestSileroVoiceActivityDetection:
    """Silero音声区間検出のテスト"""
    
    @patch('mojio.audio.silero_vad.silero_vad')
    def test_initialization(self, mock_silero_vad):
        """初期化テスト"""
        mock_model = Mock()
        mock_silero_vad.load_silero_vad.return_value = mock_model
        
        vad = SileroVoiceActivityDetection()
        vad.initialize(sample_rate=16000)
        
        # モデルがロードされたことを確認
        mock_silero_vad.load_silero_vad.assert_called_once()
        assert vad.is_initialized is True
        assert vad.sample_rate == 16000
    
    @patch('mojio.audio.silero_vad.silero_vad')
    def test_initialization_with_different_sample_rate(self, mock_silero_vad):
        """異なるサンプリングレートでの初期化テスト"""
        mock_model = Mock()
        mock_silero_vad.load_silero_vad.return_value = mock_model
        
        vad = SileroVoiceActivityDetection()
        vad.initialize(sample_rate=8000)
        
        assert vad.sample_rate == 8000
        assert vad.window_size_samples == 256
    
    def test_initialization_without_silero_vad(self):
        """silero_vadライブラリがインストールされていない場合の初期化テスト"""
        # silero_vadを無効化
        import mojio.audio.silero_vad as silero_module
        original_silero_vad = silero_module.silero_vad
        silero_module.silero_vad = None
        
        try:
            vad = SileroVoiceActivityDetection()
            with pytest.raises(RuntimeError, match="silero_vad ライブラリがインストールされていません。"):
                vad.initialize()
        finally:
            # 元に戻す
            silero_module.silero_vad = original_silero_vad
    
    @patch('mojio.audio.silero_vad.silero_vad')
    def test_is_speech_without_initialization(self, mock_silero_vad):
        """初期化せずに音声判定を実行した場合のエラーテスト"""
        vad = SileroVoiceActivityDetection()
        
        with pytest.raises(RuntimeError, match="VADモデルが初期化されていません。"):
            vad.is_speech(np.zeros(512, dtype=np.float32))
    
    @patch('mojio.audio.silero_vad.silero_vad')
    def test_is_speech_with_wrong_window_size(self, mock_silero_vad):
        """間違ったウィンドウサイズでの音声判定テスト"""
        mock_model = Mock()
        mock_silero_vad.load_silero_vad.return_value = mock_model
        
        vad = SileroVoiceActivityDetection()
        vad.initialize(sample_rate=16000)
        
        with pytest.raises(ValueError, match="音声データの長さは 512 サンプルである必要があります。"):
            vad.is_speech(np.zeros(256, dtype=np.float32))
    
    @patch('mojio.audio.silero_vad.silero_vad')
    def test_is_speech_success(self, mock_silero_vad):
        """音声判定成功テスト"""
        mock_model = Mock()
        mock_model.return_value = 0.7  # 音声確率
        mock_silero_vad.load_silero_vad.return_value = mock_model
        
        vad = SileroVoiceActivityDetection()
        vad.initialize(sample_rate=16000)
        
        audio_data = np.zeros(512, dtype=np.float32)
        result = vad.is_speech(audio_data)
        
        assert result is True
        mock_model.assert_called_once()
    
    @patch('mojio.audio.silero_vad.silero_vad')
    def test_detect_speech_segments(self, mock_silero_vad):
        """音声区間検出テスト"""
        # モックモデルの設定
        # 最初のウィンドウは音声、2番目は無音、3番目は音声
        mock_model = Mock()
        mock_model.side_effect = [0.7, 0.3, 0.8]
        mock_silero_vad.load_silero_vad.return_value = mock_model
        
        vad = SileroVoiceActivityDetection()
        vad.initialize(sample_rate=16000)
        
        # 3つのウィンドウ分の音声データを作成
        audio_data = np.zeros(512 * 3, dtype=np.float32)
        segments = vad.detect_speech_segments(audio_data)
        
        # 2つの音声区間が検出されることを確認
        # 1つ目: 0.0 - 0.032秒 (1番目のウィンドウ)
        # 2つ目: 0.064 - 0.096秒 (3番目のウィンドウ)
        assert len(segments) == 2
        assert segments[0] == (0.0, 0.032)
        assert segments[1] == (0.064, 0.096)
    
    @patch('mojio.audio.silero_vad.silero_vad')
    def test_reset(self, mock_silero_vad):
        """リセットテスト"""
        mock_model = Mock()
        mock_model.reset_states = Mock()
        mock_silero_vad.load_silero_vad.return_value = mock_model
        
        vad = SileroVoiceActivityDetection()
        vad.initialize(sample_rate=16000)
        vad.reset()
        
        # モデルのリセットメソッドが呼び出されたことを確認
        mock_model.reset_states.assert_called_once()


class TestVoiceActivityDetectionManager:
    """音声区間検出管理のテスト"""
    
    @patch('mojio.audio.silero_vad.silero_vad')
    def test_initialization(self, mock_silero_vad):
        """初期化テスト"""
        mock_model = Mock()
        mock_silero_vad.load_silero_vad.return_value = mock_model
        
        manager = VoiceActivityDetectionManager()
        manager.initialize_vad(vad_type="silero", sample_rate=16000)
        
        assert manager.current_vad_type == "silero"
        assert manager.is_active is True
        assert manager.sample_rate == 16000
    
    def test_is_speech_without_initialization(self):
        """初期化せずに音声判定を実行した場合のエラーテスト"""
        manager = VoiceActivityDetectionManager()
        
        with pytest.raises(RuntimeError, match="音声区間検出エンジンが初期化されていません。"):
            manager.is_speech(np.zeros(512, dtype=np.float32))
    
    def test_detect_speech_segments_without_initialization(self):
        """初期化せずに音声区間検出を実行した場合のエラーテスト"""
        manager = VoiceActivityDetectionManager()
        
        with pytest.raises(RuntimeError, match="音声区間検出エンジンが初期化されていません。"):
            manager.detect_speech_segments(np.zeros(512, dtype=np.float32))
    
    def test_invalid_vad_type(self):
        """無効なVADタイプでの初期化テスト"""
        manager = VoiceActivityDetectionManager()
        
        with pytest.raises(ValueError, match="サポートされていないVADエンジンタイプ"):
            manager.initialize_vad(vad_type="invalid_vad")
    
    @patch('mojio.audio.silero_vad.silero_vad')
    def test_switch_vad(self, mock_silero_vad):
        """VADエンジン切り替えテスト"""
        mock_model = Mock()
        mock_silero_vad.load_silero_vad.return_value = mock_model
        
        manager = VoiceActivityDetectionManager()
        manager.initialize_vad(vad_type="silero", sample_rate=16000)
        
        # エンジンが正しく初期化されたことを確認
        assert manager.current_vad_type == "silero"
        assert manager.is_active is True
        
        # 同じエンジンに切り替え
        manager.switch_vad(vad_type="silero", sample_rate=8000)
        
        # 新しいサンプルレートで初期化されたことを確認
        assert manager.sample_rate == 8000


if __name__ == "__main__":
    pytest.main([__file__])