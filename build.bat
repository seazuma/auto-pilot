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

echo [2/4] PyInstallerでEXEをビルド中...
pyinstaller --onefile --console --name auto_clicker auto_clicker.py
if %ERRORLEVEL% NEQ 0 (
    echo エラー: ビルドに失敗しました
    pause
    exit /b 1
)
echo.

echo [3/4] キャプチャツールをビルド中...
pyinstaller --onefile --windowed --name capture_target capture_target.py
if %ERRORLEVEL% NEQ 0 (
    echo 警告: キャプチャツールのビルドに失敗しました（スキップ）
)
echo.

echo [4/4] 設定ファイルとtargetsフォルダをdistにコピー...
copy config.json dist\config.json
copy config_advanced.json dist\config_advanced.json
xcopy /E /I /Y targets dist\targets
echo.

echo =====================================
echo ビルド完了！
echo =====================================
echo.
echo 実行ファイル:
echo   - dist\auto_clicker.exe       (メインプログラム)
echo   - dist\capture_target.exe     (標的画像キャプチャツール)
echo.
echo 設定ファイル: dist\config.json
echo 標的画像フォルダ: dist\targets\
echo.
echo 使い方:
echo 1. capture_target.exe で標的画像を作成（targetsフォルダに保存）
echo 2. config.json を編集してクリック動作を設定
echo 3. auto_clicker.exe を実行
echo.
pause
