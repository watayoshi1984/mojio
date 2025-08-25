# -*- coding: utf-8 -*-
"""
Audio Input Tests for Mojio
Mojio 音声入力テスト

音声入力モジュールのユニットテスト
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from mojio.audio.audio_input_interface import AudioInputInterface
from mojio.audio.microphone_input import MicrophoneAudioInput
from mojio.audio.loopback_input import LoopbackAudioInput
from mojio.audio.audio_manager import AudioInputManager


class TestAudioInputInterface:
    """音声入力インターフェースのテスト"""
    
    def test_interface_cannot_be_instantiated(self):
        """抽象クラスはインスタンス化できないことを確認"""
        with pytest.raises(TypeError):
            AudioInputInterface()


class TestMicrophoneAudioInput:
    """マイク音声入力のテスト"""
    
    @patch('sounddevice.query_devices')
    def test_get_device_list(self, mock_query_devices):
        """デバイス一覧取得のテスト"""
        # モックデバイスデータを設定
        mock_query_devices.return_value = [
            {
                'name': 'マイクデバイス1',
                'max_input_channels': 2,
                'default_samplerate': 44100.0
            },
            {
                'name': '出力デバイス1',
                'max_input_channels': 0,
                'default_samplerate': 48000.0
            },
            {
                'name': 'マイクデバイス2',
                'max_input_channels': 1,
                'default_samplerate': 44100.0
            }
        ]
        
        mic_input = MicrophoneAudioInput()
        devices = mic_input.get_device_list()
        
        # 入力チャンネルを持つデバイスのみが返されることを確認
        assert len(devices) == 2
        assert devices[0]['name'] == 'マイクデバイス1'
        assert devices[0]['max_input_channels'] == 2
        assert devices[1]['name'] == 'マイクデバイス2'
        assert devices[1]['max_input_channels'] == 1
    
    def test_open_stream_without_device_id(self):
        """デバイスID未指定でのストリームオープンテスト"""
        with patch('sounddevice.InputStream') as mock_stream, \
             patch('sounddevice.default') as mock_default:
            
            mock_default.device = [0, 1]  # [input_device_id, output_device_id]
            
            mic_input = MicrophoneAudioInput()
            mic_input.open_stream(sample_rate=16000, channels=1, buffer_size=1024)
            
            # InputStreamが正しいパラメータで呼び出されたことを確認
            mock_stream.assert_called_once_with(
                device=0,
                channels=1,
                samplerate=16000,
                blocksize=1024,
                dtype='float32'
            )
    
    def test_close_stream(self):
        """ストリームクローズのテスト"""
        with patch('sounddevice.InputStream') as mock_stream_class:
            mock_stream_instance = Mock()
            mock_stream_class.return_value = mock_stream_instance
            
            mic_input = MicrophoneAudioInput()
            mic_input.open_stream()
            mic_input.close_stream()
            
            # ストリームのstopとcloseが呼び出されたことを確認
            mock_stream_instance.stop.assert_called_once()
            mock_stream_instance.close.assert_called_once()
    
    def test_start_stream_without_opening(self):
        """ストリームを開かずに開始した場合のエラーテスト"""
        mic_input = MicrophoneAudioInput()
        
        with pytest.raises(RuntimeError, match="ストリームが開かれていません"):
            mic_input.start_stream(lambda x: None)


class TestLoopbackAudioInput:
    """ループバック音声入力のテスト"""
    
    @patch('soundcard.all_speakers')
    def test_get_device_list(self, mock_all_speakers):
        """デバイス一覧取得のテスト"""
        # モックスピーカーデータを設定
        mock_speaker1 = Mock()
        mock_speaker1.id = 'スピーカー1'
        mock_speaker1.name = 'スピーカー1'
        mock_speaker1.channels = 2
        
        mock_speaker2 = Mock()
        mock_speaker2.id = 'スピーカー2'
        mock_speaker2.name = 'スピーカー2'
        mock_speaker2.channels = 1
        
        mock_all_speakers.return_value = [mock_speaker1, mock_speaker2]
        
        loopback_input = LoopbackAudioInput()
        devices = loopback_input.get_device_list()
        
        assert len(devices) == 2
        assert devices[0]['id'] == 'スピーカー1'
        assert devices[0]['name'] == 'スピーカー1'
        assert devices[1]['id'] == 'スピーカー2'
        assert devices[1]['name'] == 'スピーカー2'
    
    def test_open_stream_without_device_id(self):
        """デバイスID未指定でのストリームオープンテスト"""
        with patch('soundcard.default_speaker') as mock_default_speaker, \
             patch('soundcard.get_microphone') as mock_get_microphone:
            
            mock_speaker = Mock()
            mock_speaker.id = 'デフォルトスピーカー'
            mock_default_speaker.return_value = mock_speaker
            
            loopback_input = LoopbackAudioInput()
            loopback_input.open_stream(sample_rate=16000, channels=1, buffer_size=1024)
            
            # get_microphoneが正しいパラメータで呼び出されたことを確認
            mock_get_microphone.assert_called_once_with('デフォルトスピーカー', include_loopback=True)


class TestAudioInputManager:
    """音声入力管理のテスト"""
    
    def test_initialization(self):
        """初期化テスト"""
        manager = AudioInputManager()
        
        assert isinstance(manager.microphone_input, MicrophoneAudioInput)
        assert isinstance(manager.loopback_input, LoopbackAudioInput)
        assert manager.current_input_type is None
        assert manager.is_active is False
    
    @patch('mojio.audio.microphone_input.MicrophoneAudioInput.get_device_list')
    def test_get_microphone_devices(self, mock_get_device_list):
        """マイクデバイス一覧取得テスト"""
        mock_get_device_list.return_value = [{'id': 0, 'name': 'テストマイク'}]
        
        manager = AudioInputManager()
        devices = manager.get_microphone_devices()
        
        assert len(devices) == 1
        assert devices[0]['name'] == 'テストマイク'
    
    @patch('mojio.audio.loopback_input.LoopbackAudioInput.get_device_list')
    def test_get_loopback_devices(self, mock_get_device_list):
        """ループバックデバイス一覧取得テスト"""
        mock_get_device_list.return_value = [{'id': 'テストスピーカー', 'name': 'テストスピーカー'}]
        
        manager = AudioInputManager()
        devices = manager.get_loopback_devices()
        
        assert len(devices) == 1
        assert devices[0]['name'] == 'テストスピーカー'
    
    def test_switch_input_type_invalid(self):
        """無効な入力タイプでの切り替えテスト"""
        manager = AudioInputManager()
        
        with pytest.raises(ValueError, match="input_typeは'microphone'または'loopback'である必要があります"):
            manager.switch_input_type('invalid_type')


if __name__ == "__main__":
    pytest.main([__file__])