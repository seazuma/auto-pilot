#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
マウス座標取得ツール
マウスカーソルの現在位置をリアルタイムで表示します。
Ctrl+Cで終了します。
"""

import pyautogui
import time
import sys

def main():
    print("="*60)
    print("  マウス座標取得ツール")
    print("="*60)
    print("\nマウスを動かして座標を確認してください")
    print("Ctrl+Cで終了します\n")
    print("-"*60)

    try:
        while True:
            # 現在のマウス座標を取得
            x, y = pyautogui.position()

            # 画面サイズを取得
            screen_width, screen_height = pyautogui.size()

            # 座標を表示（前の行を上書き）
            position_str = f'X: {x:4d}, Y: {y:4d}'
            screen_str = f'画面サイズ: {screen_width}x{screen_height}'

            # カーソル位置に応じたガイド
            position_guide = ""
            if x < 100 and y < 100:
                position_guide = " [左上 - 緊急停止エリア]"
            elif x < screen_width / 3:
                position_guide = " [左側]"
            elif x > screen_width * 2 / 3:
                position_guide = " [右側]"
            else:
                position_guide = " [中央]"

            print(f'\r{position_str}{position_guide} | {screen_str}', end='', flush=True)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("終了しました")
        print("="*60)
        sys.exit(0)

if __name__ == "__main__":
    main()
