# -*- coding: utf-8 -*-
"""
Whisper Speech Recognition Implementation for Mojio
Mojio Whisper音声認識実装

faster-whisperを使用した音声認識の具体実装
"""

import numpy as np
from typing import Optional, Callable, List, Iterator
from faster_whisper import WhisperModel
from .transcription_interface import SpeechRecognitionInterface, TranscriptionResult


class WhisperSpeechRecognition(SpeechRecognitionInterface):
    """
    faster-whisperを使用した音声認識実装
    
    Whisper Large v2モデルを使用して高精度な
    音声→テキスト変換を行うクラス
    """
    
    def __init__(self):
        """Whisper音声認識を初期化"""
        self.model: Optional[WhisperModel] = None
        self.model_size: str = "large-v2"
        self.device: str = "auto"
        self.compute_type: str = "float16"
        self.is_model_loaded: bool = False
        
        # サポートする言語リスト
        self.supported_languages = [
            "ja", "en", "zh", "ko", "es", "fr", "de", "it", "pt", "ru", "ar", "hi"
        ]
    
    def initialize(self, 
                  model_size: str = "large-v2",
                  device: str = "auto",
                  compute_type: str = "float16") -> None:
        """
        Whisperモデルを初期化
        
        Args:
            model_size: モデルサイズ ("tiny", "base", "small", "medium", "large-v2")
            device: 実行デバイス ("cpu", "cuda", "auto")
            compute_type: 計算精度 ("float16", "float32", "int8")
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        
        try:
            # Whisperモデルをロード
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )
            self.is_model_loaded = True
            print(f"Whisperモデル '{self.model_size}' をロードしました (デバイス: {self.device})")
        except Exception as e:
            self.is_model_loaded = False
            raise RuntimeError(f"Whisperモデルのロードに失敗しました: {e}")
    
    def transcribe(self, 
                  audio_data: np.ndarray,
                  language: Optional[str] = None) -> str:
        """
        音声データをテキストに変換
        
        Args:
            audio_data: 音声データ（numpy配列、16kHz、モノラル）
            language: 言語コード（Noneの場合は自動検出）
            
        Returns:
            str: 認識結果のテキスト
        """
        if not self.is_initialized():
            raise RuntimeError("モデルが初期化されていません。initialize()を先に呼び出してください。")
            
        if self.model is None:
            raise RuntimeError("モデルが正しくロードされていません。")
            
        try:
            # faster-whisperは32bit float、16kHzの入力を期待
            # 入力データを正規化
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
                
            # 音声認識を実行
            segments, info = self.model.transcribe(
                audio_data,
                language=language,
                beam_size=5
            )
            
            # 結果を結合
            transcription = ""
            for segment in segments:
                transcription += segment.text
                
            return transcription.strip()
            
        except Exception as e:
            raise RuntimeError(f"音声認識処理中にエラーが発生しました: {e}")
    
    def transcribe_stream(self, 
                         audio_stream: Callable[[], np.ndarray],
                         language: Optional[str] = None,
                         callback: Optional[Callable[[str], None]] = None) -> None:
        """
        ストリーム音声データをリアルタイムにテキストに変換
        
        Args:
            audio_stream: 音声データを返すコールバック関数
            language: 言語コード（Noneの場合は自動検出）
            callback: 認識結果受信時のコールバック関数
        """
        if not self.is_initialized():
            raise RuntimeError("モデルが初期化されていません。initialize()を先に呼び出してください。")
            
        if self.model is None:
            raise RuntimeError("モデルが正しくロードされていません。")
            
        try:
            # ストリームから音声データを取得して認識
            while True:
                audio_data = audio_stream()
                if audio_data is None:
                    break
                    
                # 音声認識を実行
                segments, info = self.model.transcribe(
                    audio_data,
                    language=language,
                    beam_size=5
                )
                
                # 結果を結合
                transcription = ""
                for segment in segments:
                    transcription += segment.text
                    
                # コールバック関数を呼び出す
                if callback is not None:
                    callback(transcription.strip())
                    
        except Exception as e:
            raise RuntimeError(f"ストリーム音声認識処理中にエラーが発生しました: {e}")
    
    def is_initialized(self) -> bool:
        """
        Whisperモデルが初期化されているかを返す
        
        Returns:
            bool: 初期化済みならTrue
        """
        return self.is_model_loaded and self.model is not None
    
    def get_supported_languages(self) -> List[str]:
        """
        サポートする言語一覧を取得
        
        Returns:
            List[str]: 言語コードのリスト
        """
        return self.supported_languages


# テスト用の簡単な使用例
if __name__ == "__main__":
    import time
    
    def generate_dummy_audio() -> np.ndarray:
        """テスト用のダミー音声データを生成"""
        # 1秒分の無音データ（16kHz, モノラル）
        return np.zeros(16000, dtype=np.float32)
    
    # Whisper音声認識のテスト
    whisper_recognition = WhisperSpeechRecognition()
    
    try:
        # モデルを初期化（tinyモデルでテスト）
        print("Whisperモデルを初期化中...")
        whisper_recognition.initialize(model_size="tiny", device="cpu", compute_type="float32")
        
        if whisper_recognition.is_initialized():
            print("Whisperモデルの初期化に成功しました。")
            
            # ダミー音声データでテスト
            dummy_audio = generate_dummy_audio()
            print("ダミー音声データで音声認識をテスト中...")
            
            result = whisper_recognition.transcribe(dummy_audio, language="ja")
            print(f"認識結果: {result}")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")