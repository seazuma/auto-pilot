#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
標的画像キャプチャツール
画面をスクリーンショットして、標的をマウスで選択してトリミングします
"""

import pyautogui
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import sys

TARGETS_DIR = "targets"


class ScreenshotCapture:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # メインウィンドウを隠す

        # targetsディレクトリが存在しない場合は作成
        if not os.path.exists(TARGETS_DIR):
            os.makedirs(TARGETS_DIR)
            print(f"'{TARGETS_DIR}' フォルダを作成しました")

    def capture_screenshot(self):
        """画面全体をスクリーンショット"""
        print("画面をキャプチャしています...")
        self.root.withdraw()  # ウィンドウを確実に隠す
        self.root.update()

        # 少し待ってからキャプチャ
        self.root.after(500)
        self.root.update()

        screenshot = pyautogui.screenshot()
        print("✓ キャプチャ完了")
        return screenshot

    def select_area(self, screenshot):
        """
        スクリーンショット上でマウスドラッグで領域を選択

        Returns:
            選択された領域の座標 (x1, y1, x2, y2) または None
        """
        selection_window = tk.Toplevel(self.root)
        selection_window.attributes('-fullscreen', True)
        selection_window.attributes('-topmost', True)

        # スクリーンショットを表示
        img_tk = ImageTk.PhotoImage(screenshot)
        canvas = tk.Canvas(
            selection_window,
            width=screenshot.width,
            height=screenshot.height,
            cursor="cross",
            highlightthickness=0
        )
        canvas.pack()
        canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)

        # 選択領域を描画するための矩形
        rect = None
        start_x = start_y = 0
        selected_coords = None

        # 説明テキストを表示
        instructions = canvas.create_text(
            screenshot.width // 2,
            30,
            text="マウスをドラッグして標的領域を選択してください（Escキーでキャンセル）",
            font=("Arial", 16, "bold"),
            fill="red",
            tags="instructions"
        )

        def on_mouse_down(event):
            nonlocal start_x, start_y, rect
            start_x, start_y = event.x, event.y
            if rect:
                canvas.delete(rect)
            # 説明テキストを削除
            canvas.delete("instructions")

        def on_mouse_drag(event):
            nonlocal rect
            if rect:
                canvas.delete(rect)
            rect = canvas.create_rectangle(
                start_x, start_y, event.x, event.y,
                outline="red", width=3, dash=(5, 5)
            )

        def on_mouse_up(event):
            nonlocal selected_coords
            end_x, end_y = event.x, event.y

            # 座標を正規化（左上から右下の順）
            x1 = min(start_x, end_x)
            y1 = min(start_y, end_y)
            x2 = max(start_x, end_x)
            y2 = max(start_y, end_y)

            # 最小サイズチェック
            if x2 - x1 < 10 or y2 - y1 < 10:
                messagebox.showwarning("警告", "選択領域が小さすぎます。もう一度選択してください。")
                if rect:
                    canvas.delete(rect)
                canvas.create_text(
                    screenshot.width // 2,
                    30,
                    text="マウスをドラッグして標的領域を選択してください（Escキーでキャンセル）",
                    font=("Arial", 16, "bold"),
                    fill="red",
                    tags="instructions"
                )
                return

            selected_coords = (x1, y1, x2, y2)
            selection_window.quit()

        def on_escape(event):
            nonlocal selected_coords
            selected_coords = None
            selection_window.quit()

        canvas.bind("<ButtonPress-1>", on_mouse_down)
        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_mouse_up)
        selection_window.bind("<Escape>", on_escape)

        selection_window.mainloop()
        selection_window.destroy()

        return selected_coords

    def save_cropped_image(self, screenshot, coords):
        """
        選択領域をトリミングして保存

        Args:
            screenshot: PIL Image
            coords: (x1, y1, x2, y2)
        """
        # ファイル名を入力
        filename = simpledialog.askstring(
            "ファイル名入力",
            "標的画像のファイル名を入力してください:\n（例: button_ok.png）",
            parent=self.root
        )

        if not filename:
            print("キャンセルされました")
            return False

        # 拡張子がない場合は .png を追加
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            filename += '.png'

        # 画像をトリミング
        cropped = screenshot.crop(coords)

        # 保存パス
        save_path = os.path.join(TARGETS_DIR, filename)

        # 既に同名ファイルがある場合は確認
        if os.path.exists(save_path):
            overwrite = messagebox.askyesno(
                "確認",
                f"'{filename}' は既に存在します。\n上書きしますか？"
            )
            if not overwrite:
                print("キャンセルされました")
                return False

        # 保存
        cropped.save(save_path)
        print(f"\n✓ 保存しました: {save_path}")
        print(f"  サイズ: {cropped.width} x {cropped.height} px")

        # プレビューを表示
        self.show_preview(cropped, filename)

        return True

    def show_preview(self, image, filename):
        """保存した画像のプレビューを表示"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"プレビュー: {filename}")

        # 画像が大きい場合は縮小
        max_size = 400
        img_copy = image.copy()
        if img_copy.width > max_size or img_copy.height > max_size:
            img_copy.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(img_copy)

        frame = tk.Frame(preview_window, padx=10, pady=10)
        frame.pack()

        label = tk.Label(frame, image=img_tk)
        label.image = img_tk  # 参照を保持
        label.pack()

        info_text = f"ファイル: {filename}\nサイズ: {image.width} x {image.height} px"
        info_label = tk.Label(frame, text=info_text, justify=tk.LEFT)
        info_label.pack(pady=5)

        ok_button = tk.Button(
            frame,
            text="OK",
            command=preview_window.destroy,
            padx=20,
            pady=5
        )
        ok_button.pack(pady=5)

        preview_window.transient(self.root)
        preview_window.grab_set()
        self.root.wait_window(preview_window)

    def run(self):
        """メイン処理"""
        print("="*60)
        print("  標的画像キャプチャツール")
        print("="*60)
        print()
        print("このツールで標的画像を作成できます:")
        print("1. 画面全体がキャプチャされます")
        print("2. マウスドラッグで標的領域を選択します")
        print("3. ファイル名を入力して保存します")
        print()

        response = messagebox.askyesno(
            "確認",
            "画面をキャプチャします。\n\n準備ができたら「はい」をクリックしてください。\n\n※ このウィンドウは自動的に隠れます"
        )

        if not response:
            print("キャンセルされました")
            return

        # スクリーンショットを撮る
        screenshot = self.capture_screenshot()

        # 領域を選択
        coords = self.select_area(screenshot)

        if coords is None:
            print("キャンセルされました")
            return

        # トリミングして保存
        if self.save_cropped_image(screenshot, coords):
            # 続けて作成するか確認
            another = messagebox.askyesno(
                "確認",
                "標的画像を保存しました。\n\n続けて別の標的を作成しますか？"
            )
            if another:
                self.run()  # 再帰的に呼び出し

        self.root.destroy()


def main():
    try:
        app = ScreenshotCapture()
        app.run()
        print("\n終了しました")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        input("\nEnterキーで終了...")
        sys.exit(1)


if __name__ == "__main__":
    main()
