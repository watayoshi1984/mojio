# Mojio（もじ夫）- AIで文字起こしを高精度に

🎙️ **思考と対話を加速する、インテリジェント・リアルタイム・トランスクライバー**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://doc.qt.io/qtforpython/)
[![Whisper Large v2](https://img.shields.io/badge/AI-Whisper%20Large%20v2-orange.svg)](https://github.com/SYSTRAN/faster-whisper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 概要

Mojio（もじ夫）は、Whisper Large v2エンジンを使用した高精度な**リアルタイム文字起こしアプリケーション**です。  
PC上のあらゆる音声を即座にテキスト化し、任意のアプリケーションに直接挿入できます。

### ✨ 主な特徴

- 🔊 **デュアル音声対応**: マイク + PC内部音声の同時キャプチャ
- ⚡ **リアルタイム処理**: 平均1.5秒以内の高速変換
- 🔒 **完全オフライン**: プライバシー重視の設計
- 🎯 **ユニバーサル対応**: 任意のアプリケーションで動作
- 📚 **ユーザー辞書**: 専門用語・固有名詞の高精度認識
- ⌨️ **グローバルショートカット**: `Ctrl+Shift+Space`でどこからでも起動

## 🎯 対象ユーザー

- **開発者・エンジニア**: コード作成、技術文書の効率化
- **営業・企画職**: 会議の議事録作成、顧客ヒアリング
- **研究者・学生**: セミナー受講、文献整理
- **ライター・クリエイター**: アイデア記録、執筆支援
- **アクセシビリティ**: 聴覚サポートが必要な方

## 🎬 使用例

### オンライン会議での使用
```
[Ctrl+Shift+Space] → 録音開始
話者: 「来週の製品リリースに向けて、APIの最終テストを行います」
→ 即座にテキスト化され、議事録に自動入力
```

### コード作成時の支援
```
[Ctrl+Shift+Space] → 録音開始
開発者: 「ユーザー認証のためのJWTトークン生成関数を作成」
→ IDEのコメント欄に正確にテキスト挿入
```

## 🛠️ 技術スタック

| カテゴリ | 技術 | 目的 |
|---------|------|------|
| **言語** | Python 3.10+ | 高い開発効率と豊富なAIライブラリ |
| **GUI** | PySide6 | モダンで高機能なユーザーインターフェース |
| **音声認識** | faster-whisper | Whisper Large v2の高速化版 |
| **音声I/O** | SoundDevice, SoundCard | マイク・PC音声の統合キャプチャ |
| **システム統合** | pynput | グローバルショートカット・テキスト挿入 |
| **データ管理** | SQLite3, PyYAML | ユーザー辞書・設定・履歴管理 |

## 📦 インストール

### 必要な環境
- **OS**: Windows 10/11, macOS 10.15+
- **Python**: 3.10以上
- **メモリ**: 4GB以上推奨
- **ストレージ**: 2GB以上の空き容量

### クイックスタート

```bash
# 1. リポジトリをクローン
git clone https://github.com/mojio-dev/mojio.git
cd mojio

# 2. 仮想環境作成（推奨）
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 依存関係インストール
pip install -r requirements.txt

# 4. アプリケーション起動
python src/main.py
```

### 開発環境セットアップ

```bash
# 開発用依存関係を含めてインストール
pip install -r requirements-dev.txt

# コード品質チェック
black src/
flake8 src/
mypy src/

# テスト実行
pytest tests/
```

## 🎮 使用方法

### 基本操作

1. **アプリケーション起動**: `python src/main.py`
2. **音声入力開始**: `Ctrl+Shift+Space`
3. **話す**: マイクに向かって自然に話す
4. **テキスト挿入**: アクティブなテキストフィールドに自動挿入
5. **録音停止**: 再度 `Ctrl+Shift+Space` または無音検出で自動停止

### 高度な機能

- **ユーザー辞書**: 専門用語を事前登録で認識精度向上
- **音源切替**: マイク⇔PC内部音声の動的切替
- **履歴機能**: 過去の文字起こし結果を検索・再利用
- **プロファイル**: 用途別設定（会議用・メモ用など）

## 📈 開発ロードマップ

### フェーズ1: プロトタイプ（1ヶ月）✅
- [x] 基本GUI実装
- [x] 音声キャプチャ機能
- [x] faster-whisper統合
- [x] テキスト挿入機能
- [x] グローバルショートカット

### フェーズ2: インテリジェント機能（2ヶ月）🚧
- [ ] PC内部音声対応
- [ ] ユーザー辞書システム
- [ ] 高度VAD機能
- [ ] UI/UX改善

### フェーズ3: 完成度向上（2ヶ月）📋
- [ ] アダプティブUI
- [ ] 履歴・検索機能
- [ ] プロファイル管理
- [ ] パフォーマンス最適化
- [ ] 配布パッケージ作成

## 🤝 貢献

プロジェクトへの貢献を歓迎します！

1. Issues での機能要望・バグ報告
2. Pull Requests での機能実装・修正
3. ドキュメントの改善
4. テストケースの追加

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

## 🙏 謝辞

- [OpenAI Whisper](https://github.com/openai/whisper) - 優秀な音声認識モデル
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) - 高速化実装
- [PySide6](https://doc.qt.io/qtforpython/) - 優れたGUIフレームワーク

---

**Mojio Development Team** | 📧 dev@mojio.local | 🌐 [GitHub](https://github.com/watayoshi1984/mojio)