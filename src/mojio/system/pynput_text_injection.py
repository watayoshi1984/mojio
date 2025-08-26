# -*- coding: utf-8 -*-
"""
Pynput Text Injection Implementation for Mojio
Mojio Pynputテキスト挿入実装

pynputを使用したテキスト挿入の具体実装
"""

import time
from typing import Optional
from pynput.keyboard import Controller, Key
from pynput import keyboard
import pygetwindow as gw


class PynputTextInjection:
    """
    pynputを使用したテキスト挿入実装
    
    キーボードイベントをシミュレートして
    アクティブウィンドウにテキストを挿入するクラス
    """
    
    def __init__(self):
        """pynputテキスト挿入を初期化"""
        self.keyboard_controller = Controller()
        self.typing_delay: float = 0.01  # 文字間の遅延（秒）
        self.delay_before: float = 0.1   # 挿入前の遅延（秒）
        
    def inject_text(self, text: str, target_window: Optional[str] = None) -> bool:
        """
        指定されたテキストをアクティブまたは指定されたウィンドウに挿入
        
        Args:
            text: 挿入するテキスト
            target_window: ターゲットウィンドウ名（Noneの場合はアクティブウィンドウ）
            
        Returns:
            bool: 挿入成功ならTrue、失敗ならFalse
        """
        try:
            # 指定されたウィンドウにフォーカスを移動（オプション）
            if target_window is not None:
                self._focus_window(target_window)
            
            # 挿入前の遅延
            if self.delay_before > 0:
                time.sleep(self.delay_before)
            
            # テキストを1文字ずつ入力
            for char in text:
                self.keyboard_controller.press(char)
                self.keyboard_controller.release(char)
                
                # 文字間の遅延
                if self.typing_delay > 0:
                    time.sleep(self.typing_delay)
                    
            return True
            
        except Exception as e:
            print(f"テキスト挿入エラー: {e}")
            return False
    
    def inject_text_with_clipboard(self, text: str, target_window: Optional[str] = None) -> bool:
        """
        クリップボードを使用してテキストを挿入
        
        Args:
            text: 挿入するテキスト
            target_window: ターゲットウィンドウ名（Noneの場合はアクティブウィンドウ）
            
        Returns:
            bool: 挿入成功ならTrue、失敗ならFalse
        """
        try:
            import pyperclip
            
            # 指定されたウィンドウにフォーカスを移動（オプション）
            if target_window is not None:
                self._focus_window(target_window)
            
            # 現在のクリップボード内容を保存
            original_clipboard = pyperclip.paste()
            
            # テキストをクリップボードにコピー
            pyperclip.copy(text)
            
            # 挿入前の遅延
            if self.delay_before > 0:
                time.sleep(self.delay_before)
            
            # Ctrl+Vで貼り付け
            with self.keyboard_controller.pressed(Key.ctrl):
                self.keyboard_controller.press('v')
                self.keyboard_controller.release('v')
                
            # 元のクリップボード内容を復元
            time.sleep(0.1)  # 貼り付けが完了するのを待つ
            pyperclip.copy(original_clipboard)
            
            return True
            
        except Exception as e:
            print(f"クリップボード使用テキスト挿入エラー: {e}")
            return False
    
    def _focus_window(self, window_title: str) -> bool:
        """
        指定されたタイトルのウィンドウにフォーカスを移動
        
        Args:
            window_title: ウィンドウタイトル
            
        Returns:
            bool: フォーカス移動成功ならTrue、失敗ならFalse
        """
        try:
            # ウィンドウを検索
            windows = gw.getWindowsWithTitle(window_title)
            if windows:
                # 最初に見つかったウィンドウにフォーカスを移動
                window = windows[0]
                window.activate()
                return True
            return False
        except Exception as e:
            print(f"ウィンドウフォーカスエラー: {e}")
            return False
    
    def get_active_window_title(self) -> str:
        """
        現在アクティブなウィンドウのタイトルを取得
        
        Returns:
            str: アクティブウィンドウのタイトル
        """
        try:
            # 現在アクティブなウィンドウを取得
            active_window = gw.getActiveWindow()
            if active_window:
                return active_window.title
            return ""
        except Exception as e:
            print(f"アクティブウィンドウタイトル取得エラー: {e}")
            return ""
    
    def is_text_input_available(self) -> bool:
        """
        現在のウィンドウでテキスト入力が可能かどうかを判定
        
        Returns:
            bool: テキスト入力が可能ならTrue
        """
        try:
            # アクティブウィンドウのタイトルを取得
            title = self.get_active_window_title()
            
            # 明らかにテキスト入力が不可能なウィンドウを除外
            # （実際のアプリケーションではより詳細な判定が必要）
            if any(keyword in title.lower() for keyword in ["desktop", "explorer", "finder"]):
                return False
                
            return True
        except Exception as e:
            print(f"テキスト入力可否判定エラー: {e}")
            return True  # デフォルトでは可能と仮定
    
    def set_typing_delay(self, delay: float) -> None:
        """
        文字入力間の遅延を設定
        
        Args:
            delay: 遅延時間（秒）
        """
        self.typing_delay = delay
    
    def set_delay_before(self, delay: float) -> None:
        """
        テキスト挿入前の遅延を設定
        
        Args:
            delay: 遅延時間（秒）
        """
        self.delay_before = delay


# テスト用の簡単な使用例
if __name__ == "__main__":
    import time
    
    # テキスト挿入のテスト
    text_injector = PynputTextInjection()
    
    try:
        # アクティブウィンドウのタイトルを表示
        active_window = text_injector.get_active_window_title()
        print(f"アクティブウィンドウ: {active_window}")
        
        # テキスト入力が可能かどうかを確認
        if text_injector.is_text_input_available():
            print("テキスト入力が可能です。")
            
            # 3秒待機（ユーザーがテキストエディタに切り替える時間）
            print("3秒後にテストテキストを挿入します。テキストエディタに切り替えてください...")
            time.sleep(3)
            
            # テストテキストを挿入
            test_text = "これはMojioからのテストメッセージです。"
            success = text_injector.inject_text(test_text)
            
            if success:
                print("テキスト挿入に成功しました。")
            else:
                print("テキスト挿入に失敗しました。")
        else:
            print("現在のウィンドウではテキスト入力ができません。")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")