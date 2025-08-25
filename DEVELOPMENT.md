# 開発ガイドライン - Mojio（もじ夫）

## 🎯 プロジェクト概要

**Mojio（もじ夫）** は、Whisper Large v2エンジンを使用した高精度なリアルタイム文字起こしアプリケーションです。  
AIで文字起こしを高精度に行い、任意のアプリケーションにリアルタイムでテキストを挿入できます。

## 🛠️ 開発環境セットアップ

### 必要な環境
- **Python**: 3.10以上
- **OS**: Windows 10/11, macOS 10.15+
- **メモリ**: 4GB以上推奨
- **ストレージ**: 2GB以上の空き容量

### クイックスタート

#### 1. 自動セットアップ（推奨）

**Windows:**
```cmd
setup_dev_env.bat
```

**Unix/Linux/macOS:**
```bash
chmod +x setup_dev_env.sh
./setup_dev_env.sh
```

#### 2. 手動セットアップ

```bash
# 1. 仮想環境作成
python -m venv venv

# 2. 仮想環境アクティベート
# Windows:
venv\Scripts\activate
# Unix/Linux/macOS:
source venv/bin/activate

# 3. 依存関係インストール
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. 開発モードでインストール
pip install -e .
```

#### 3. UV使用（高速）

```bash
# 1. UV インストール（未インストールの場合）
pip install uv

# 2. 仮想環境作成・依存関係インストール
uv venv venv
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
```

## 🚀 アプリケーション起動

```bash
# 仮想環境をアクティベート後
python src/main.py
```

## 🧪 テスト実行

```bash
# 全テスト実行
pytest

# GUI テストのみ
pytest tests/test_gui.py

# カバレッジ付きテスト
pytest --cov=src/mojio tests/
```

## 📁 プロジェクト構造

```
mojio/
├── src/
│   ├── mojio/
│   │   ├── __init__.py
│   │   ├── gui/           # GUIコンポーネント
│   │   ├── audio/         # 音声処理
│   │   ├── system/        # システム統合
│   │   └── data/          # データ管理
│   └── main.py            # メインエントリーポイント
├── tests/                 # テストコード
├── config/                # 設定ファイル
├── requirements.txt       # 本番依存関係
├── requirements-dev.txt   # 開発依存関係
├── pyproject.toml         # プロジェクト設定
└── README.md              # プロジェクト説明
```

## 🎨 コーディング規約

### Python スタイル
- **PEP 8** に準拠
- **Black** でフォーマット: `black src/`
- **Flake8** でリント: `flake8 src/`
- **mypy** で型チェック: `mypy src/`

### 命名規則
- **関数/変数**: `snake_case`
- **クラス**: `PascalCase`
- **定数**: `UPPER_CASE`
- **プライベート**: `_leading_underscore`

### ドキュメント
- **関数/クラス**: Google スタイルの docstring
- **型ヒント**: 全ての関数に型アノテーション

### 例：
```python
def transcribe_audio(audio_data: np.ndarray, language: str = "ja") -> str:
    """
    音声データを文字起こしする
    
    Args:
        audio_data: 音声データ配列
        language: 言語コード（デフォルト: "ja"）
        
    Returns:
        文字起こし結果テキスト
        
    Raises:
        AudioProcessingError: 音声処理エラー時
    """
    # ... 実装 ...
```

## 🔧 開発ワークフロー

### 1. 機能開発
```bash
# 1. ブランチ作成
git checkout -b feature/新機能名

# 2. 開発・テスト
python src/main.py
pytest

# 3. コード品質チェック
black src/ tests/
flake8 src/ tests/
mypy src/

# 4. コミット・プッシュ
git add .
git commit -m "feat: 新機能の説明"
git push origin feature/新機能名
```

### 2. バグ修正
```bash
# 1. バグ修正ブランチ
git checkout -b fix/バグ修正名

# 2. 修正・テスト
# ... 修正作業 ...
pytest

# 3. コミット
git commit -m "fix: バグ修正の説明"
```

### 3. コミットメッセージ規約
- `feat:` 新機能
- `fix:` バグ修正  
- `docs:` ドキュメント
- `style:` フォーマット
- `refactor:` リファクタリング
- `test:` テスト追加
- `chore:` その他

## 🏗️ 技術スタック

| カテゴリ | 技術 | 用途 |
|---------|------|------|
| **言語** | Python 3.10+ | メイン開発言語 |
| **GUI** | PySide6 | ユーザーインターフェース |
| **音声認識** | faster-whisper | Whisper Large v2エンジン |
| **音声I/O** | SoundDevice, SoundCard | 音声キャプチャ |
| **システム** | pynput | ショートカット・テキスト挿入 |
| **データ** | SQLite3, PyYAML | DB・設定管理 |
| **テスト** | pytest, pytest-qt | テストフレームワーク |

## 🐛 デバッグ・トラブルシューティング

### よくある問題

#### 1. PySide6 インストールエラー
```bash
# Qt6 ライブラリが見つからない場合
pip install --upgrade PySide6
```

#### 2. 音声デバイスエラー
```bash
# 音声デバイス一覧確認
python -c "import sounddevice as sd; print(sd.query_devices())"
```

#### 3. faster-whisper モデルダウンロードエラー
```bash
# プロキシ環境の場合
export HTTPS_PROXY=http://proxy.example.com:8080
```

### ログ確認
```bash
# アプリケーションログ
tail -f logs/mojio.log

# デバッグモード起動
python src/main.py --debug
```

## 📈 パフォーマンス最適化

### プロファイリング
```bash
# メモリ使用量チェック
python -m memory_profiler src/main.py

# CPU使用量チェック  
python -m cProfile -o profile.prof src/main.py
```

### 最適化のポイント
1. **音声処理**: NumPy配列の効率的使用
2. **GUI**: 不要な再描画の削減
3. **メモリ**: ガベージコレクションの調整
4. **I/O**: 非同期処理の活用

## 🚢 配布・デプロイ

### 実行ファイル作成
```bash
# PyInstaller で実行ファイル化
pyinstaller --onefile --windowed src/main.py --name "Mojio"
```

### インストーラー作成
```bash
# Windows: Inno Setup使用
# macOS: create-dmg使用
```

## 🤝 コントリビューション

1. Issues での機能要望・バグ報告
2. Pull Requests での機能実装・修正
3. ドキュメントの改善
4. テストケースの追加

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

---

**Happy Coding! 🎙️ Mojio（もじ夫）で効率的な音声入力を実現しましょう！**