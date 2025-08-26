# -*- coding: utf-8 -*-
"""
Custom Exceptions for MOJIO
MOJIO用カスタム例外

プロジェクト全体で使用するカスタム例外クラスを定義
"""

class MojioBaseException(Exception):
    """MOJIOアプリケーションの基本例外クラス"""
    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class AudioInputError(MojioBaseException):
    """音声入力関連のエラー"""
    def __init__(self, message: str):
        super().__init__(message, "AUDIO_INPUT_ERROR")


class SpeechRecognitionError(MojioBaseException):
    """音声認識関連のエラー"""
    def __init__(self, message: str):
        super().__init__(message, "SPEECH_RECOGNITION_ERROR")


class TextInjectionError(MojioBaseException):
    """テキスト挿入関連のエラー"""
    def __init__(self, message: str):
        super().__init__(message, "TEXT_INJECTION_ERROR")


class DatabaseError(MojioBaseException):
    """データベース関連のエラー"""
    def __init__(self, message: str):
        super().__init__(message, "DATABASE_ERROR")


class ConfigurationError(MojioBaseException):
    """設定関連のエラー"""
    def __init__(self, message: str):
        super().__init__(message, "CONFIGURATION_ERROR")


class ValidationError(MojioBaseException):
    """データ検証関連のエラー"""
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class InitializationError(MojioBaseException):
    """初期化関連のエラー"""
    def __init__(self, message: str):
        super().__init__(message, "INITIALIZATION_ERROR")


class FileNotFoundError(MojioBaseException):
    """ファイル関連のエラー"""
    def __init__(self, message: str):
        super().__init__(message, "FILE_NOT_FOUND_ERROR")


class PermissionError(MojioBaseException):
    """権限関連のエラー"""
    def __init__(self, message: str):
        super().__init__(message, "PERMISSION_ERROR")


class NetworkError(MojioBaseException):
    """ネットワーク関連のエラー"""
    def __init__(self, message: str):
        super().__init__(message, "NETWORK_ERROR")


class TimeoutError(MojioBaseException):
    """タイムアウト関連のエラー"""
    def __init__(self, message: str):
        super().__init__(message, "TIMEOUT_ERROR")