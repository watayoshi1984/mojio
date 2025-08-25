@echo off
rem setup_dev_env.bat
rem Mojio（もじ夫）開発環境セットアップスクリプト（Windows用）

echo 🎙️ Mojio（もじ夫）開発環境セットアップを開始します...

rem Python バージョンチェック
echo 📋 Python バージョンを確認中...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python が見つかりません。Python 3.10以上をインストールしてください。
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

echo ✅ Python が見つかりました。

rem UV のチェック
echo 🔍 UV が利用可能かチェック中...
uv --version >nul 2>&1
if %errorlevel% eq 0 (
    echo 🚀 UV を使用して仮想環境を作成します...
    uv venv venv
    echo 📦 UV で依存関係をインストールします...
    uv pip install -r requirements.txt
    uv pip install -r requirements-dev.txt
) else (
    echo 🏗️ venv を使用して仮想環境を作成します...
    %PYTHON_CMD% -m venv venv
    
    rem 仮想環境をアクティベート
    call venv\Scripts\activate.bat
    
    rem pip アップグレード
    echo 📈 pip をアップグレード中...
    python -m pip install --upgrade pip
    
    rem 依存関係インストール
    echo 📦 依存関係をインストール中...
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
)

echo.
echo ✅ セットアップ完了！
echo.
echo 🚀 開発を開始するには：
echo    1. 仮想環境をアクティベート:
echo       venv\Scripts\activate
echo.
echo    2. アプリケーションを起動:
echo       python src\main.py
echo.
echo    3. テストを実行:
echo       pytest tests\
echo.
pause