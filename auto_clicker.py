#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows自動クリックツール（画像認識版）
設定ファイル(config.json)を読み込んで、画像認識で標的を探してクリックします
"""

import pyautogui
import json
import time
import sys
import os
from pathlib import Path

# PyAutoGUIの安全機能: マウスを画面の隅に移動すると緊急停止
pyautogui.FAILSAFE = True

# 標的画像を保存するフォルダ
TARGETS_DIR = "targets"


class AutoClicker:
    def __init__(self, config_path="config.json"):
        """
        自動クリッカーを初期化

        Args:
            config_path: 設定ファイルのパス
        """
        self.config_path = config_path
        self.actions = []

    def load_config(self):
        """設定ファイルを読み込む"""
        if not os.path.exists(self.config_path):
            print(f"エラー: 設定ファイル '{self.config_path}' が見つかりません")
            return False

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.actions = config.get('actions', [])
                print(f"✓ 設定ファイルを読み込みました: {len(self.actions)}個のアクション")
                return True
        except json.JSONDecodeError as e:
            print(f"エラー: 設定ファイルのJSON形式が正しくありません: {e}")
            return False
        except Exception as e:
            print(f"エラー: 設定ファイルの読み込みに失敗しました: {e}")
            return False

    def find_image(self, image_name, confidence=0.8, grayscale=False, timeout=5):
        """
        画面上で画像を検索

        Args:
            image_name: 画像ファイル名
            confidence: 一致度 (0.0-1.0)
            grayscale: グレースケールで検索（高速化）
            timeout: タイムアウト時間（秒）

        Returns:
            見つかった場合は座標のタプル (x, y)、見つからない場合はNone
        """
        image_path = os.path.join(TARGETS_DIR, image_name)

        if not os.path.exists(image_path):
            print(f"\nエラー: 画像ファイル '{image_path}' が見つかりません")
            return None

        start_time = time.time()
        attempt = 0

        while time.time() - start_time < timeout:
            attempt += 1
            try:
                location = pyautogui.locateCenterOnScreen(
                    image_path,
                    confidence=confidence,
                    grayscale=grayscale
                )

                if location is not None:
                    return location

                # 短い間隔で再試行
                if time.time() - start_time < timeout:
                    time.sleep(0.5)

            except pyautogui.ImageNotFoundException:
                if time.time() - start_time < timeout:
                    time.sleep(0.5)
                continue
            except Exception as e:
                print(f"\n画像検索エラー: {e}")
                return None

        return None

    def execute_action(self, action, index):
        """
        1つのアクションを実行

        Args:
            action: アクションの辞書
            index: アクションのインデックス
        """
        action_type = action.get('type', 'click')

        print(f"\n[{index + 1}] {action_type}: ", end='')

        try:
            if action_type == 'click_image':
                # 画像認識でクリック
                image = action.get('image')
                button = action.get('button', 'left')
                clicks = action.get('clicks', 1)
                confidence = action.get('confidence', 0.8)
                grayscale = action.get('grayscale', False)
                timeout = action.get('timeout', 5)
                offset_x = action.get('offset_x', 0)
                offset_y = action.get('offset_y', 0)

                if not image:
                    print(f"エラー: 画像ファイル名が指定されていません")
                    return False

                print(f"画像 '{image}' を検索中...", end='', flush=True)
                location = self.find_image(image, confidence, grayscale, timeout)

                if location is None:
                    print(f" 見つかりませんでした（タイムアウト: {timeout}秒）")
                    return False

                # オフセットを適用
                click_x = location[0] + offset_x
                click_y = location[1] + offset_y

                print(f" 発見! ({location[0]}, {location[1]})")
                print(f"    → 座標({click_x}, {click_y})を{button}ボタンで{clicks}回クリック")
                pyautogui.click(click_x, click_y, clicks=clicks, button=button)

            elif action_type == 'wait_for_image':
                # 画像が表示されるまで待機
                image = action.get('image')
                confidence = action.get('confidence', 0.8)
                grayscale = action.get('grayscale', False)
                timeout = action.get('timeout', 30)

                if not image:
                    print(f"エラー: 画像ファイル名が指定されていません")
                    return False

                print(f"画像 '{image}' が表示されるまで待機（最大{timeout}秒）...", end='', flush=True)
                location = self.find_image(image, confidence, grayscale, timeout)

                if location is None:
                    print(f" タイムアウト")
                    return False

                print(f" 発見! ({location[0]}, {location[1]})")

            elif action_type == 'click':
                # 座標指定でクリック（従来の方式）
                x = action.get('x')
                y = action.get('y')
                button = action.get('button', 'left')
                clicks = action.get('clicks', 1)

                if x is None or y is None:
                    print(f"エラー: 座標(x, y)が指定されていません")
                    return False

                print(f"座標({x}, {y})を{button}ボタンで{clicks}回クリック")
                pyautogui.click(x, y, clicks=clicks, button=button)

            elif action_type == 'wait':
                seconds = action.get('seconds', 1)
                print(f"{seconds}秒待機")
                time.sleep(seconds)

            elif action_type == 'move':
                x = action.get('x')
                y = action.get('y')
                duration = action.get('duration', 0.5)

                if x is None or y is None:
                    print(f"エラー: 座標(x, y)が指定されていません")
                    return False

                print(f"座標({x}, {y})へ{duration}秒かけて移動")
                pyautogui.moveTo(x, y, duration=duration)

            elif action_type == 'type':
                text = action.get('text', '')
                interval = action.get('interval', 0.05)
                print(f"テキスト入力: '{text}'")
                pyautogui.typewrite(text, interval=interval)

            elif action_type == 'hotkey':
                keys = action.get('keys', [])
                print(f"ホットキー: {'+'.join(keys)}")
                pyautogui.hotkey(*keys)

            elif action_type == 'press':
                key = action.get('key', '')
                presses = action.get('presses', 1)
                print(f"キー '{key}' を{presses}回押下")
                pyautogui.press(key, presses=presses)

            elif action_type == 'scroll':
                amount = action.get('amount', 0)
                x = action.get('x')
                y = action.get('y')
                if x is not None and y is not None:
                    print(f"座標({x}, {y})で{amount}スクロール")
                    pyautogui.scroll(amount, x=x, y=y)
                else:
                    print(f"{amount}スクロール")
                    pyautogui.scroll(amount)

            else:
                print(f"警告: 不明なアクションタイプ '{action_type}'")
                return False

            return True

        except Exception as e:
            print(f"\nエラー: アクション実行中に問題が発生しました: {e}")
            return False

    def run(self, start_delay=3):
        """
        すべてのアクションを順番に実行

        Args:
            start_delay: 開始前の待機時間(秒)
        """
        if not self.actions:
            print("実行するアクションがありません")
            return

        print(f"\n{start_delay}秒後に開始します...")
        print("※ 緊急停止: マウスを画面の左上隅に移動してください")

        for i in range(start_delay, 0, -1):
            print(f"{i}...", end=' ', flush=True)
            time.sleep(1)
        print("\n\n開始!\n" + "="*50)

        try:
            for index, action in enumerate(self.actions):
                if not self.execute_action(action, index):
                    print(f"\nアクション #{index + 1} でエラーが発生しました")
                    break

            print("\n" + "="*50)
            print("✓ すべてのアクションが完了しました")

        except pyautogui.FailSafeException:
            print("\n\n緊急停止: ユーザーによって中断されました")
        except KeyboardInterrupt:
            print("\n\n中断: Ctrl+Cが押されました")
        except Exception as e:
            print(f"\n\nエラー: 予期しない問題が発生しました: {e}")


def main():
    print("="*50)
    print("  Windows自動クリックツール")
    print("="*50)

    # コマンドライン引数から設定ファイルのパスを取得
    config_path = "config.json"
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    clicker = AutoClicker(config_path)

    if not clicker.load_config():
        print("\n使い方: auto_clicker.exe [設定ファイル]")
        print("例: auto_clicker.exe config.json")
        input("\nEnterキーを押して終了...")
        sys.exit(1)

    # 設定内容のサマリーを表示
    print("\n設定内容:")
    print("-"*50)
    for i, action in enumerate(clicker.actions):
        action_type = action.get('type', 'click')
        if action_type == 'click_image':
            print(f"{i+1}. 画像クリック - '{action.get('image')}'")
        elif action_type == 'wait_for_image':
            print(f"{i+1}. 画像待機 - '{action.get('image')}'")
        elif action_type == 'click':
            print(f"{i+1}. クリック - 座標({action.get('x')}, {action.get('y')})")
        elif action_type == 'wait':
            print(f"{i+1}. 待機 - {action.get('seconds')}秒")
        elif action_type == 'move':
            print(f"{i+1}. 移動 - 座標({action.get('x')}, {action.get('y')})")
        elif action_type == 'type':
            print(f"{i+1}. 入力 - '{action.get('text')}'")
        else:
            print(f"{i+1}. {action_type}")
    print("-"*50)

    try:
        input("\nEnterキーを押して開始 (Ctrl+Cで中止)...")
    except KeyboardInterrupt:
        print("\n中止されました")
        sys.exit(0)

    clicker.run(start_delay=3)

    input("\n\nEnterキーを押して終了...")


if __name__ == "__main__":
    main()
