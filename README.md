# Windows自動クリックツール（画像認識版）

**画像認識**で標的を探して自動的にクリックするWindowsツールです。座標指定は不要！

## 特徴

- ✅ **画像認識**: 標的画像を探して自動クリック - 座標指定不要
- ✅ **簡単な標的作成**: スクリーンショット＆トリミングツール付属
- ✅ **柔軟な設定**: JSON形式の設定ファイルで挙動を自由にカスタマイズ
- ✅ **スタンドアロン実行**: コンパイル済みEXEファイルなので特別なソフトは不要
- ✅ **豊富な機能**: 画像クリック、待機、テキスト入力、ホットキー、スクロールなど
- ✅ **安全性**: 緊急停止機能付き（マウスを画面左上に移動で停止）

## クイックスタート

### 📸 ステップ1: 標的画像を作成

1. `capture_target.bat`を実行（またはPythonで`capture_target.py`を実行）
2. 画面全体がキャプチャされます
3. マウスでドラッグして、クリックしたい標的（ボタンなど）を選択
4. ファイル名を入力（例: `button_ok.png`）
5. 標的画像が`targets`フォルダに保存されます

### ⚙️ ステップ2: 設定ファイルを編集

`config.json`をテキストエディタで開いて、標的画像とアクションを設定：

```json
{
  "actions": [
    {
      "type": "click_image",
      "image": "button_ok.png",
      "note": "OKボタンをクリック"
    },
    {
      "type": "wait",
      "seconds": 1
    },
    {
      "type": "click_image",
      "image": "button_next.png",
      "note": "次へボタンをクリック"
    }
  ]
}
```

### ▶️ ステップ3: 実行

- **ビルド済みEXE**: `auto_clicker.exe`をダブルクリック
- **Python**: `python auto_clicker.py`を実行

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

### 🎯 1. 画像クリック (`click_image`) ★推奨★

画像認識で標的を探してクリックします。

```json
{
  "type": "click_image",
  "image": "button_ok.png",
  "button": "left",
  "clicks": 1,
  "confidence": 0.8,
  "timeout": 5,
  "offset_x": 0,
  "offset_y": 0,
  "grayscale": false,
  "note": "OKボタンをクリック"
}
```

**パラメータ:**
- `image` (必須): `targets`フォルダ内の画像ファイル名
- `button`: `"left"` (左), `"right"` (右), `"middle"` (中央) - デフォルト: `"left"`
- `clicks`: クリック回数 - デフォルト: `1`
- `confidence`: 一致度 (0.0-1.0) - デフォルト: `0.8`（80%）
- `timeout`: 検索タイムアウト（秒）- デフォルト: `5`
- `offset_x`: クリック位置のX軸オフセット（ピクセル）- デフォルト: `0`
- `offset_y`: クリック位置のY軸オフセット（ピクセル）- デフォルト: `0`
- `grayscale`: グレースケールで検索（高速化）- デフォルト: `false`

**Tips:**
- 標的が見つかりにくい場合は`confidence`を下げてください（例: `0.7`）
- 高速化したい場合は`grayscale: true`にしてください
- ボタンの中心からずらしたい場合は`offset_x`/`offset_y`を使用

### 🕐 2. 画像待機 (`wait_for_image`)

指定した画像が画面に表示されるまで待機します。

```json
{
  "type": "wait_for_image",
  "image": "dialog_confirm.png",
  "confidence": 0.8,
  "timeout": 30,
  "grayscale": false,
  "note": "確認ダイアログが表示されるまで待機"
}
```

**パラメータ:**
- `image` (必須): 待機する画像ファイル名
- `confidence`: 一致度 (0.0-1.0) - デフォルト: `0.8`
- `timeout`: タイムアウト時間（秒）- デフォルト: `30`
- `grayscale`: グレースケールで検索 - デフォルト: `false`

### 3. 座標クリック (`click`)

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

## 📸 標的画像の作成方法

### 方法1: キャプチャツールを使用（推奨）

1. **`capture_target.bat`を実行**
2. 「はい」をクリック
3. 画面全体がキャプチャされ、全画面表示されます
4. **マウスでドラッグ**して、クリックしたい標的（ボタン、アイコンなど）を選択
5. ファイル名を入力（例: `button_submit.png`）
6. `targets`フォルダに保存されます

**Tips:**
- ボタン全体を選択するよりも、**特徴的な部分だけ**を選択する方が認識しやすいです
- 背景が変わらない部分を選択してください
- 小さすぎると見つかりにくいので、適度なサイズで選択

### 方法2: 手動でスクリーンショット

1. `Win + Shift + S`（Windows Snipping Tool）でスクリーンショット
2. 画像編集ソフト（ペイントなど）でボタン部分をトリミング
3. PNG形式で`targets`フォルダに保存

### 標的画像作成のコツ

✅ **良い例:**
- ボタンのテキスト部分だけをトリミング
- アイコンの特徴的な部分
- 色やデザインが特徴的な部分

❌ **悪い例:**
- ボタン全体＋背景
- 動的に変わる可能性がある部分
- 小さすぎる画像（10px以下など）

### 標的が見つからない場合

1. **confidenceを下げる**: `0.8` → `0.7` または `0.6`
2. **grayscaleを有効化**: `"grayscale": true`
3. **標的画像を作り直す**: より特徴的な部分を選択
4. **画像サイズを調整**: 大きすぎても小さすぎても見つかりにくい

## サンプル設定

### 例1: 基本的な画像クリック操作

```json
{
  "actions": [
    {"type": "wait", "seconds": 1},
    {"type": "click_image", "image": "button_start.png"},
    {"type": "wait", "seconds": 0.5},
    {"type": "click_image", "image": "button_next.png", "clicks": 1}
  ]
}
```

### 例2: 画像待機とテキスト入力

```json
{
  "actions": [
    {
      "type": "wait_for_image",
      "image": "login_screen.png",
      "timeout": 10,
      "note": "ログイン画面が表示されるまで待機"
    },
    {
      "type": "click_image",
      "image": "username_field.png",
      "note": "ユーザー名入力欄をクリック"
    },
    {"type": "wait", "seconds": 0.3},
    {"type": "hotkey", "keys": ["ctrl", "a"], "note": "全選択"},
    {"type": "type", "text": "myusername"},
    {"type": "press", "key": "tab"},
    {"type": "type", "text": "mypassword"},
    {
      "type": "click_image",
      "image": "button_login.png",
      "note": "ログインボタンをクリック"
    }
  ]
}
```

### 例3: 繰り返し処理

同じボタンを複数回クリックする場合：

```json
{
  "actions": [
    {"type": "click_image", "image": "button_collect.png"},
    {"type": "wait", "seconds": 2},
    {"type": "click_image", "image": "button_collect.png"},
    {"type": "wait", "seconds": 2},
    {"type": "click_image", "image": "button_collect.png"}
  ]
}
```

### 例4: エラー処理付き

```json
{
  "actions": [
    {
      "type": "click_image",
      "image": "button_start.png",
      "timeout": 10,
      "note": "開始ボタンを10秒間探す"
    },
    {
      "type": "wait_for_image",
      "image": "processing_icon.png",
      "timeout": 30,
      "note": "処理中アイコンが表示されるまで待機"
    },
    {
      "type": "wait_for_image",
      "image": "complete_dialog.png",
      "timeout": 60,
      "note": "完了ダイアログを待機"
    },
    {
      "type": "click_image",
      "image": "button_ok.png",
      "confidence": 0.9,
      "note": "OKボタンをクリック（高精度）"
    }
  ]
}
```

## 安全機能

### 緊急停止

実行中にマウスカーソルを**画面の左上隅**に移動すると、プログラムが緊急停止します。

### 開始遅延

プログラムは実行後、3秒間の遅延があります。この間にウィンドウを切り替えたり、準備を整えることができます。

## トラブルシューティング

### 問題: 標的画像が見つからない

**原因と解決策:**

1. **画像の一致度が低い**
   - `confidence`を下げる: `0.8` → `0.7` または `0.6`
   ```json
   {"type": "click_image", "image": "button.png", "confidence": 0.7}
   ```

2. **画面の解像度やスケールが異なる**
   - Windowsの表示スケール設定を確認: 設定 → ディスプレイ → 拡大縮小
   - 標的画像を実際の画面で作り直す

3. **標的画像が小さすぎる/大きすぎる**
   - 適度なサイズ（30x30px以上推奨）で作り直す
   - ボタン全体ではなく、特徴的な部分だけを切り取る

4. **背景や色が変わっている**
   - グレースケールで検索: `"grayscale": true`
   - より特徴的な部分を選択して標的画像を作り直す

5. **タイムアウトが短すぎる**
   - `timeout`を長くする: `"timeout": 10` （10秒）

### 問題: 検索が遅い

**解決策:**
- グレースケール検索を有効化: `"grayscale": true`
- 標的画像のサイズを小さくする（ただし小さすぎないように）
- `confidence`を高めに設定（例: `0.9`）

### 問題: 間違った場所をクリックする

**解決策:**
- 標的画像をより特徴的な部分だけに絞る
- `confidence`を高くする: `"confidence": 0.9`
- `offset_x`/`offset_y`でクリック位置を微調整

### 問題: テキスト入力が正しく動作しない

**解決策:**
- 英数字のみをサポートしています
- 日本語入力がオンの場合は、先にIMEをオフにしてください
  ```json
  {"type": "hotkey", "keys": ["alt", "`"]}
  ```

### 問題: EXEファイルが実行できない

**解決策:**
- Windows Defenderに検出される場合があります
- 信頼できる場合は、除外設定を追加してください

### 問題: 画像が保存されない

**解決策:**
- `targets`フォルダが存在するか確認
- ファイル名に使用できない文字（\ / : * ? " < > |）を含んでいないか確認

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
├── auto_clicker.py            # メインプログラム（画像認識版）
├── capture_target.py          # 標的画像キャプチャツール
├── capture_target.bat         # キャプチャツール起動バッチ
├── get_coordinates.py         # 座標確認ツール（参考用）
├── get_coordinates.bat        # 座標ツール起動バッチ
├── config.json                # 基本設定ファイル（画像認識用）
├── config_advanced.json       # 高度な設定例
├── requirements.txt           # Python依存関係
├── build.bat                  # Windowsビルドスクリプト
├── build.ps1                  # PowerShellビルドスクリプト
├── README.md                  # このファイル
├── targets/                   # 標的画像フォルダ
│   ├── .gitkeep
│   ├── button_ok.png          # 例: OKボタンの画像
│   ├── button_next.png        # 例: 次へボタンの画像
│   └── ...                    # その他の標的画像
└── dist/                      # ビルド後の実行ファイル（ビルド後に作成）
    ├── auto_clicker.exe
    ├── capture_target.exe
    ├── config.json
    └── targets/               # 標的画像もコピーされます
```

### コードのカスタマイズ

`auto_clicker.py`を編集することで、新しいアクションタイプを追加できます。

新しいアクションの追加例：
```python
elif action_type == 'custom_action':
    # カスタムアクションの実装
    print("カスタムアクション実行")
```
