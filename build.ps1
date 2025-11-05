# Windows自動クリックツールのビルドスクリプト (PowerShell版)
#
# 使用方法:
# 1. Pythonをインストール (https://www.python.org/)
# 2. PowerShellでこのスクリプトを実行: .\build.ps1
# 3. dist フォルダ内に auto_clicker.exe が生成されます

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " Windows自動クリックツール - ビルド" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# エラーが発生したら停止
$ErrorActionPreference = "Stop"

try {
    Write-Host "[1/3] 依存関係のインストール..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        throw "依存関係のインストールに失敗しました"
    }
    Write-Host ""

    Write-Host "[2/4] メインプログラムをビルド中..." -ForegroundColor Yellow
    pyinstaller --onefile --console --name auto_clicker auto_clicker.py
    if ($LASTEXITCODE -ne 0) {
        throw "ビルドに失敗しました"
    }
    Write-Host ""

    Write-Host "[3/4] キャプチャツールをビルド中..." -ForegroundColor Yellow
    pyinstaller --onefile --windowed --name capture_target capture_target.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "警告: キャプチャツールのビルドに失敗しました（スキップ）" -ForegroundColor Yellow
    }
    Write-Host ""

    Write-Host "[4/4] 設定ファイルとtargetsフォルダをコピー..." -ForegroundColor Yellow
    Copy-Item -Path "config.json" -Destination "dist\config.json" -Force
    Copy-Item -Path "config_advanced.json" -Destination "dist\config_advanced.json" -Force
    if (Test-Path "targets") {
        Copy-Item -Path "targets" -Destination "dist\targets" -Recurse -Force
    }
    Write-Host ""

    Write-Host "=====================================" -ForegroundColor Green
    Write-Host " ビルド完了！" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "実行ファイル:" -ForegroundColor Cyan
    Write-Host "  - dist\auto_clicker.exe       " -NoNewline -ForegroundColor Green
    Write-Host "(メインプログラム)"
    Write-Host "  - dist\capture_target.exe     " -NoNewline -ForegroundColor Green
    Write-Host "(標的画像キャプチャツール)"
    Write-Host ""
    Write-Host "設定ファイル: " -NoNewline
    Write-Host "dist\config.json" -ForegroundColor Green
    Write-Host "標的画像フォルダ: " -NoNewline
    Write-Host "dist\targets\" -ForegroundColor Green
    Write-Host ""
    Write-Host "使い方:" -ForegroundColor Cyan
    Write-Host "1. capture_target.exe で標的画像を作成（targetsフォルダに保存）"
    Write-Host "2. config.json を編集してクリック動作を設定"
    Write-Host "3. auto_clicker.exe を実行"
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "エラー: $_" -ForegroundColor Red
    Write-Host ""
    exit 1
}

Write-Host "Enterキーを押して終了..."
Read-Host
