# -*- coding: utf-8 -*-
"""
Text Injection Manager for Mojio
Mojio テキスト挿入管理

テキスト挿入機能の統合管理クラス
"""

from typing import Optional
from .text_injection_interface import TextInjectionInterface
from .pynput_text_injection import PynputTextInjection


class TextInjectionManager:
    """
    テキスト挿入機能の統合管理クラス
    
    複数のテキスト挿入方法を管理し、
    統一されたインターフェースでテキスト挿入機能を提供
    """
    
    def __init__(self):
        """テキスト挿入管理を初期化"""
        self.pynput_injector = PynputTextInjection()
        self.current_injector: TextInjectionInterface = self.pynput_injector
        self.current_method: str = "pynput_typing"
        self.is_active: bool = True
        
        # デフォルト設定
        self.typing_delay: float = 0.01
        self.delay_before: float = 0.1
        
        # 設定を適用
        self.pynput_injector.set_typing_delay(self.typing_delay)
        self.pynput_injector.set_delay_before(self.delay_before)
    
    def inject_text(self, text: str, target_window: Optional[str] = None) -> bool:
        """
        指定されたテキストをアクティブまたは指定されたウィンドウに挿入
        
        Args:
            text: 挿入するテキスト
            target_window: ターゲットウィンドウ名（Noneの場合はアクティブウィンドウ）
            
        Returns:
            bool: 挿入成功ならTrue、失敗ならFalse
        """
        if not self.is_active:
            return False
            
        if self.current_method == "pynput_typing":
            return self.pynput_injector.inject_text(text, target_window)
        elif self.current_method == "pynput_clipboard":
            return self.pynput_injector.inject_text_with_clipboard(text, target_window)
        else:
            raise ValueError(f"サポートされていない挿入方法: {self.current_method}")
    
    def inject_text_with_method(self, text: str, method: str, target_window: Optional[str] = None) -> bool:
        """
        指定された方法でテキストを挿入
        
        Args:
            text: 挿入するテキスト
            method: 挿入方法 ("pynput_typing", "pynput_clipboard")
            target_window: ターゲットウィンドウ名（Noneの場合はアクティブウィンドウ）
            
        Returns:
            bool: 挿入成功ならTrue、失敗ならFalse
        """
        original_method = self.current_method
        self.switch_method(method)
        
        try:
            result = self.inject_text(text, target_window)
            return result
        finally:
            # 元の方法に戻す
            self.switch_method(original_method)
    
    def get_active_window_title(self) -> str:
        """
        現在アクティブなウィンドウのタイトルを取得
        
        Returns:
            str: アクティブウィンドウのタイトル
        """
        return self.pynput_injector.get_active_window_title()
    
    def is_text_input_available(self) -> bool:
        """
        現在のウィンドウでテキスト入力が可能かどうかを判定
        
        Returns:
            bool: テキスト入力が可能ならTrue
        """
        return self.pynput_injector.is_text_input_available()
    
    def switch_method(self, method: str) -> None:
        """
        テキスト挿入方法を切り替える
        
        Args:
            method: 挿入方法 ("pynput_typing", "pynput_clipboard")
        """
        if method not in ["pynput_typing", "pynput_clipboard"]:
            raise ValueError(f"サポートされていない挿入方法: {method}")
            
        self.current_method = method
    
    def set_typing_delay(self, delay: float) -> None:
        """
        文字入力間の遅延を設定
        
        Args:
            delay: 遅延時間（秒）
        """
        self.typing_delay = delay
        self.pynput_injector.set_typing_delay(delay)
    
    def set_delay_before(self, delay: float) -> None:
        """
        テキスト挿入前の遅延を設定
        
        Args:
            delay: 遅延時間（秒）
        """
        self.delay_before = delay
        self.pynput_injector.set_delay_before(delay)


# テスト用の簡単な使用例
if __name__ == "__main__":
    import time
    
    # テキスト挿入管理のテスト
    injection_manager = TextInjectionManager()
    
    try:
        # アクティブウィンドウのタイトルを表示
        active_window = injection_manager.get_active_window_title()
        print(f"アクティブウィンドウ: {active_window}")
        
        # テキスト入力が可能かどうかを確認
        if injection_manager.is_text_input_available():
            print("テキスト入力が可能です。")
            
            # 3秒待機（ユーザーがテキストエディタに切り替える時間）
            print("3秒後にテストテキストを挿入します。テキストエディタに切り替えてください...")
            time.sleep(3)
            
            # テストテキストを挿入
            test_text = "これはMojioのテキスト挿入管理からのテストメッセージです。"
            success = injection_manager.inject_text(test_text)
            
            if success:
                print("テキスト挿入に成功しました。")
            else:
                print("テキスト挿入に失敗しました。")
        else:
            print("現在のウィンドウではテキスト入力ができません。")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")