#!/bin/bash
# setup_dev_env.sh
# Mojio（もじ夫）開発環境セットアップスクリプト

echo "🎙️ Mojio（もじ夫）開発環境セットアップを開始します..."

# Python バージョンチェック
echo "📋 Python バージョンを確認中..."
python --version || py --version || python3 --version

# 仮想環境作成
echo "🏗️  仮想環境を作成中..."
if command -v uv &> /dev/null; then
    echo "UV を使用して仮想環境を作成します..."
    uv venv venv
    echo "UV で依存関係をインストールします..."
    uv pip install -r requirements.txt
    uv pip install -r requirements-dev.txt
else
    echo "venv を使用して仮想環境を作成します..."
    python -m venv venv || py -m venv venv || python3 -m venv venv
    
    # 仮想環境をアクティベート（Windows）
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
        echo "Windows 環境で仮想環境をアクティベートしました"
    else
        source venv/bin/activate
        echo "Unix 環境で仮想環境をアクティベートしました"
    fi
    
    # pip アップグレード
    python -m pip install --upgrade pip
    
    # 依存関係インストール
    echo "📦 依存関係をインストール中..."
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
fi

echo "✅ セットアップ完了！"
echo ""
echo "🚀 開発を開始するには："
echo "   1. 仮想環境をアクティベート:"
echo "      Windows: venv\\Scripts\\activate"
echo "      Unix: source venv/bin/activate"
echo ""
echo "   2. アプリケーションを起動:"
echo "      python src/main.py"
echo ""
echo "   3. テストを実行:"
echo "      pytest tests/"