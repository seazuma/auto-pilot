@echo off
REM Windows自動クリックツールのビルドスクリプト
REM
REM 使用方法:
REM 1. Pythonをインストール (https://www.python.org/)
REM 2. このバッチファイルを実行
REM 3. dist フォルダ内に auto_clicker.exe が生成されます

echo =====================================
echo Windows自動クリックツール - ビルド
echo =====================================
echo.

echo [1/3] 依存関係のインストール...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo エラー: 依存関係のインストールに失敗しました
    pause
    exit /b 1
)
echo.

echo [2/3] PyInstallerでEXEをビルド中...
pyinstaller --onefile --windowed --name auto_clicker --icon=NONE auto_clicker.py
if %ERRORLEVEL% NEQ 0 (
    echo エラー: ビルドに失敗しました
    pause
    exit /b 1
)
echo.

echo [3/3] 設定ファイルをdistフォルダにコピー...
copy config.json dist\config.json
copy config_advanced.json dist\config_advanced.json
echo.

echo =====================================
echo ビルド完了！
echo =====================================
echo.
echo 実行ファイル: dist\auto_clicker.exe
echo 設定ファイル: dist\config.json
echo.
echo 使い方:
echo 1. config.json を編集してクリック動作を設定
echo 2. auto_clicker.exe を実行
echo.
pause
