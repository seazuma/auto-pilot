# Windows自動クリックツール

設定ファイル（JSON）で指定した順序で、自動的にマウスクリックやキーボード操作を実行するWindowsツールです。

## 特徴

- ✅ **簡単な設定**: JSON形式の設定ファイルで挙動を自由にカスタマイズ
- ✅ **スタンドアロン実行**: コンパイル済みEXEファイルなので特別なソフトは不要
- ✅ **豊富な機能**: クリック、待機、移動、テキスト入力、ホットキー、スクロールなど
- ✅ **安全性**: 緊急停止機能付き（マウスを画面左上に移動で停止）

## クイックスタート

### 方法1: ビルド済みEXEを使用（推奨）

1. `dist`フォルダ内の`auto_clicker.exe`と`config.json`を任意のフォルダにコピー
2. `config.json`をテキストエディタで編集して動作を設定
3. `auto_clicker.exe`をダブルクリックで実行

### 方法2: Pythonから実行

```bash
# 依存関係をインストール
pip install -r requirements.txt

# 実行
python auto_clicker.py
```

## ビルド方法

Pythonがインストールされている環境で、以下のいずれかを実行：

### Windows バッチファイル
```cmd
build.bat
```

### PowerShell
```powershell
.\build.ps1
```

ビルドが完了すると、`dist`フォルダに`auto_clicker.exe`が生成されます。

## 設定ファイルの編集

`config.json`をテキストエディタ（メモ帳など）で開いて編集します。

### 基本構造

```json
{
  "actions": [
    {
      "type": "アクションの種類",
      "パラメータ1": "値1",
      "パラメータ2": "値2",
      "note": "説明（オプション）"
    }
  ]
}
```

## 使用可能なアクション

### 1. クリック (`click`)

指定した座標をクリックします。

```json
{
  "type": "click",
  "x": 500,
  "y": 300,
  "button": "left",
  "clicks": 1,
  "note": "座標(500, 300)を左クリック"
}
```

**パラメータ:**
- `x` (必須): X座標
- `y` (必須): Y座標
- `button`: `"left"` (左), `"right"` (右), `"middle"` (中央) - デフォルト: `"left"`
- `clicks`: クリック回数 - デフォルト: `1`

### 2. 待機 (`wait`)

指定した秒数待機します。

```json
{
  "type": "wait",
  "seconds": 2.5,
  "note": "2.5秒待機"
}
```

**パラメータ:**
- `seconds` (必須): 待機時間（秒）。小数点も使用可能

### 3. マウス移動 (`move`)

マウスカーソルを指定座標に移動します。

```json
{
  "type": "move",
  "x": 800,
  "y": 500,
  "duration": 0.5,
  "note": "0.5秒かけて移動"
}
```

**パラメータ:**
- `x` (必須): 移動先のX座標
- `y` (必須): 移動先のY座標
- `duration`: 移動にかける時間（秒）- デフォルト: `0.5`

### 4. テキスト入力 (`type`)

英数字のテキストを入力します（日本語は非対応）。

```json
{
  "type": "type",
  "text": "Hello World",
  "interval": 0.05,
  "note": "テキストを入力"
}
```

**パラメータ:**
- `text` (必須): 入力するテキスト（英数字のみ）
- `interval`: キー入力の間隔（秒）- デフォルト: `0.05`

### 5. ホットキー (`hotkey`)

複数のキーを同時押しします（Ctrl+C、Alt+Tabなど）。

```json
{
  "type": "hotkey",
  "keys": ["ctrl", "c"],
  "note": "Ctrl+C（コピー）"
}
```

**パラメータ:**
- `keys` (必須): 同時押しするキーのリスト

**よく使うホットキーの例:**
- コピー: `["ctrl", "c"]`
- 貼り付け: `["ctrl", "v"]`
- 全選択: `["ctrl", "a"]`
- 保存: `["ctrl", "s"]`
- ウィンドウ切り替え: `["alt", "tab"]`

### 6. キー押下 (`press`)

特定のキーを押します。

```json
{
  "type": "press",
  "key": "enter",
  "presses": 1,
  "note": "Enterキーを押す"
}
```

**パラメータ:**
- `key` (必須): 押すキー（`"enter"`, `"delete"`, `"tab"`, `"esc"`, など）
- `presses`: 押す回数 - デフォルト: `1`

### 7. スクロール (`scroll`)

マウスホイールでスクロールします。

```json
{
  "type": "scroll",
  "amount": -3,
  "note": "上に3スクロール"
}
```

**パラメータ:**
- `amount` (必須): スクロール量（正=下、負=上）
- `x`: スクロール位置のX座標（オプション）
- `y`: スクロール位置のY座標（オプション）

## 座標の確認方法

マウスカーソルの座標を確認するには、以下の方法があります：

1. **Windowsの標準ツールを使用**
   - ペイント (Paint) を開いて、マウスを動かすと左下に座標が表示されます

2. **PowerShell**で座標を表示
   ```powershell
   Add-Type -AssemblyName System.Windows.Forms
   while($true) {
       $pos = [System.Windows.Forms.Cursor]::Position
       Write-Host "`rX: $($pos.X), Y: $($pos.Y)" -NoNewline
       Start-Sleep -Milliseconds 100
   }
   ```

3. **Python**で座標を表示（PyAutoGUIインストール済みの場合）
   ```python
   import pyautogui
   import time
   try:
       while True:
           x, y = pyautogui.position()
           print(f'\rX: {x}, Y: {y}', end='')
           time.sleep(0.1)
   except KeyboardInterrupt:
       print('\n終了')
   ```

## サンプル設定

### 例1: 基本的なクリック操作

```json
{
  "actions": [
    {"type": "wait", "seconds": 1},
    {"type": "click", "x": 500, "y": 300},
    {"type": "wait", "seconds": 0.5},
    {"type": "click", "x": 700, "y": 400, "clicks": 2}
  ]
}
```

### 例2: テキスト入力とホットキー

```json
{
  "actions": [
    {"type": "click", "x": 300, "y": 200, "note": "入力欄をクリック"},
    {"type": "wait", "seconds": 0.3},
    {"type": "hotkey", "keys": ["ctrl", "a"], "note": "全選択"},
    {"type": "press", "key": "delete"},
    {"type": "type", "text": "Hello World"},
    {"type": "press", "key": "enter"}
  ]
}
```

### 例3: 繰り返しクリック

同じ座標を複数回クリックする場合：

```json
{
  "actions": [
    {"type": "click", "x": 500, "y": 300},
    {"type": "wait", "seconds": 1},
    {"type": "click", "x": 500, "y": 300},
    {"type": "wait", "seconds": 1},
    {"type": "click", "x": 500, "y": 300}
  ]
}
```

## 安全機能

### 緊急停止

実行中にマウスカーソルを**画面の左上隅**に移動すると、プログラムが緊急停止します。

### 開始遅延

プログラムは実行後、3秒間の遅延があります。この間にウィンドウを切り替えたり、準備を整えることができます。

## トラブルシューティング

### 問題: クリック位置がずれる

**解決策:** Windowsの表示スケール設定を確認してください
- 設定 → システム → ディスプレイ → 拡大縮小
- 100%以外の場合、座標がずれることがあります

### 問題: テキスト入力が正しく動作しない

**解決策:**
- 英数字のみをサポートしています
- 日本語入力がオンになっている場合は、先にホットキーでIMEをオフにしてください
- 例: `{"type": "hotkey", "keys": ["alt", "~"]}`（IME切り替え）

### 問題: EXEファイルが実行できない

**解決策:**
- Windows Defenderに検出される場合があります
- 信頼できる場合は、除外設定を追加してください

## 注意事項

⚠️ **このツールの使用について**
- 自動化する操作が利用規約に違反しないか確認してください
- ゲームやアプリケーションによっては、自動操作が禁止されている場合があります
- 本ツールの使用は自己責任でお願いします

## 技術仕様

- **言語**: Python 3.x
- **主要ライブラリ**: PyAutoGUI
- **ビルドツール**: PyInstaller
- **対応OS**: Windows 10/11
- **設定形式**: JSON

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## サポート

問題や質問がある場合は、GitHubのIssuesページで報告してください。

---

**開発者向け情報**

### ディレクトリ構造

```
auto-pilot/
├── auto_clicker.py         # メインプログラム
├── config.json             # 基本設定ファイル
├── config_advanced.json    # 高度な設定例
├── requirements.txt        # Python依存関係
├── build.bat              # Windowsビルドスクリプト
├── build.ps1              # PowerShellビルドスクリプト
├── README.md              # このファイル
└── dist/                  # ビルド後の実行ファイル（ビルド後に作成）
    ├── auto_clicker.exe
    └── config.json
```

### コードのカスタマイズ

`auto_clicker.py`を編集することで、新しいアクションタイプを追加できます。

新しいアクションの追加例：
```python
elif action_type == 'custom_action':
    # カスタムアクションの実装
    print("カスタムアクション実行")
```
