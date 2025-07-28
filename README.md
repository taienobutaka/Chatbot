# AI チャットボット - テキスト解析機能付き

Python で開発されたシンプルな AI チャットボットです。テキストメッセージの解析と理解機能を備えています。

![メイン画面](<スクリーンショット 2025-07-28 141703.png>)

## � 目次

- [🚀 機能](#-機能)
- [🛠️ 技術スタック](#️-技術スタック)
- [📁 プロジェクト構造](#-プロジェクト構造)
- [🛠️ インストール・セットアップ](#️-インストールセットアップ)
- [🚀 クイックスタート](#-クイックスタート)
- [🌐 アクセス情報](#-アクセス情報)
- [🛠️ Makefile コマンド一覧](#️-makefile-コマンド一覧)
- [📊 データベーススキーマ](#-データベーススキーマ)
- [🤖 AI 機能の詳細](#-ai-機能の詳細)
- [🔧 カスタマイズ](#-カスタマイズ)
- [🚨 トラブルシューティング](#-トラブルシューティング)
- [📈 今後の改善計画](#-今後の改善計画)

## �🚀 機能

### 基本機能

- リアルタイムチャット
- 会話履歴の保存と読み込み
- レスポンシブ Web デザイン

### AI 機能

- **テキスト解析**: メッセージの解析と理解
- **感情分析**: positive/negative/neutral の感情判定
- **意図分類**: 挨拶、別れ、感謝などの意図を自動分類
- **キーワード抽出**: 重要なキーワードを自動抽出
- **インテリジェント応答**: 分析結果に基づく適切な応答生成

### 分析機能

- リアルタイム分析結果表示
- 感情分析統計
- 意図分類統計
- 会話パターン分析

## 🛠️ 技術スタック

### Backend

- **Python**: 3.11
- **Flask**: 2.3.3
- **Gunicorn**: 21.2.0 (WSGI サーバー)

### Database

- **PostgreSQL**: 15 (Alpine)
- **psycopg2**: 2.9.7 (PostgreSQL アダプター)

### Frontend

- **HTML5/CSS3/JavaScript**: バニラ実装
- **レスポンシブデザイン**: CSS Grid & Flexbox

### Container & Infrastructure

- **Docker**: Latest
- **Docker Compose**: 3.8
- **pgAdmin**: 4 (Latest)

### AI/ML Libraries

- **NLTK**: 3.8.1 (自然言語処理)
- **scikit-learn**: 1.3.0 (機械学習)
- **NumPy**: 1.24.3 (数値計算)
- **pandas**: 2.0.3 (データ分析)
- **TextBlob**: 0.17.1 (テキスト処理)

### Text Analysis

- **TF-IDF**: Term Frequency-Inverse Document Frequency
- **Cosine Similarity**: コサイン類似度計算
- **パターンマッチング**: 正規表現ベース

## 📁 プロジェクト構造

```
Python/
├── app.py                 # メインアプリケーション (Flask 2.3.3)
├── docker-compose.yml    # Docker Compose設定 (v3.8)
├── Dockerfile            # Docker設定 (Python 3.11-slim ベース)
├── Makefile              # 効率的な開発・運用コマンド
├── requirements.txt      # Python依存関係定義
├── init.sql              # PostgreSQL初期化スクリプト
├── start.sh              # レガシー起動スクリプト
├── .env                  # 環境変数設定
├── .gitignore           # Git除外設定
├── pgadmin-servers.json  # pgAdmin自動設定
├── templates/
│   └── chat.html        # Jinja2 HTMLテンプレート
├── static/
│   ├── css/
│   │   └── style.css    # レスポンシブCSS
│   └── js/
│       └── chat.js      # バニラJavaScript
├── backups/              # DB バックアップ (make db-backup)
└── README.md            # プロジェクトドキュメント
```

### 🏗️ アーキテクチャ概要

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   Database      │
│                 │    │                  │    │                 │
│ HTML/CSS/JS     │◄──►│ Flask 2.3.3      │◄──►│ PostgreSQL 15   │
│ (Port 80)       │    │ Python 3.11      │    │ (Port 5432)     │
│                 │    │ NLTK + ML        │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Management     │
                       │                  │
                       │ pgAdmin 4        │
                       │ (Port 8080)      │
                       └──────────────────┘
```

## 🛠️ インストール・セットアップ

### 📦 リポジトリのクローン

このプロジェクトを使用するには、まず GitHub からリポジトリをクローンしてください：

#### SSH 接続（推奨）

```bash
# SSHキーが設定済みの場合
git clone git@github.com:taienobutaka/Chatbot.git
cd Chatbot
```

#### HTTPS 接続

```bash
# HTTPSでクローン
git clone https://github.com/taienobutaka/Chatbot.git
cd Chatbot
```

### ⚡ 必要な環境

以下がインストールされていることを確認してください：

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Git**: 2.0+
- **Make**: 任意（Makefile コマンドを使用する場合）

### 🔧 環境確認

```bash
# Docker バージョン確認
docker --version
docker-compose --version

# Git バージョン確認
git --version

# Make バージョン確認（任意）
make --version
```

## 🚀 クイックスタート

### 🔥 完全自動セットアップ（推奨）

リポジトリをクローンした後、たった 1 つのコマンドで全て完了します：

```bash
# リポジトリクローン後のディレクトリで実行
make start
```

**これだけで以下が自動実行されます：**

- ✅ Docker 環境のチェック
- ✅ 必要なイメージのビルド
- ✅ PostgreSQL データベースの初期化
- ✅ pgAdmin の設定
- ✅ チャットボットアプリケーションの起動
- ✅ ヘルスチェックの実行

### 📱 アクセス確認

起動完了後、以下のコマンドでブラウザを開けます：

```bash
make open         # チャットボット（http://localhost）
make open-pgadmin # pgAdmin（http://localhost:8080）
```

### ⚡ 開発者向けクイックスタート

```bash
# 開発モードで起動（ログ表示付き）
make dev

# 基本機能テスト
make test

# サービス状態確認
make status
```

### 🎯 手動セットアップ（従来方式）

Makefile を使わない場合：

```bash
# 1. 環境構築・起動
docker-compose up --build -d

# 2. ログ確認
docker-compose logs -f chatbot

# 3. ブラウザでアクセス
# http://localhost - チャットボット
# http://localhost:8080 - pgAdmin
```

### 📋 利用可能な主要コマンド

```bash
make help          # 全コマンドの説明を表示
make start         # 🚀 完全セットアップ（初回推奨）
make dev           # 🛠️ 開発モードで起動（ログ表示）
make test          # 🧪 基本機能テスト
make status        # 📊 サービス状態確認
make logs          # 📋 ログ表示
make restart       # 🔄 再起動
make reset         # 🔄 完全リセット&再構築
make clean         # 🧹 不要なリソース削除
```

## 🚀 従来の起動方法

### 1. 自動起動（推奨）

```bash
# 起動スクリプトに実行権限を付与
chmod +x start.sh

# チャットボットを起動
./start.sh
```

### 2. 手動起動

```bash
# Docker Composeでビルド＆起動
docker-compose up --build -d

# ログ確認
docker-compose logs -f chatbot
```

## 🌐 アクセス情報

起動後、以下の URL にアクセスできます:

### 🤖 チャットボットアプリケーション

- **メインアプリ**: http://localhost (ポート 80)
- **ヘルスチェック**: http://localhost/health
- **API エンドポイント**: http://localhost/api/chat

### 🗄️ データベース管理 (pgAdmin 4)

- **管理画面**: http://localhost:8080 (ポート 8080)
- **メールアドレス**: admin@admin.com
- **パスワード**: admin

### 🔗 PostgreSQL 接続設定（pgAdmin 内で新サーバー登録時）

| 項目                         | 値           |
| ---------------------------- | ------------ |
| **ホスト名/アドレス**        | postgres     |
| **ポート**                   | 5432         |
| **メンテナンスデータベース** | postgres     |
| **ユーザー名**               | chatbot_user |
| **パスワード**               | chatbot_pass |

### 📊 データベース直接接続（外部ツール用）

- **ホスト**: localhost
- **ポート**: 5432
- **データベース**: chatbot_db
- **ユーザー**: chatbot_user
- **パスワード**: chatbot_pass

## �️ Makefile コマンド一覧

本プロジェクトでは、開発効率を向上させるため、包括的な Makefile を提供しています。以下のコマンドで様々な操作を効率的に実行できます。

### 🚀 クイックスタート

```bash
make               # ヘルプ表示
make start         # 完全セットアップ（初回推奨）
make dev           # 開発モード起動（ログ表示付き）
make stop          # サービス停止
```

### 🔄 ライフサイクル管理

```bash
make build         # Dockerイメージビルド
make up            # サービス起動
make down          # サービス停止＆削除
make restart       # サービス再起動
make reset         # 完全リセット＆再構築
```

### 📊 監視・ログ確認

```bash
make status        # サービス状態確認
make health        # ヘルスチェック実行
make logs          # 全サービスログ表示
make logs-chatbot  # チャットボットログのみ
make logs-db       # データベースログのみ
make logs-pgadmin  # pgAdminログのみ
```

### 🗄️ データベース操作

```bash
make db-connect    # PostgreSQL直接接続
make db-backup     # データベースバックアップ
make db-reset      # データベースリセット
make open-pgadmin  # pgAdmin Webインターフェース起動
```

### 🧪 テスト・検証

```bash
make test          # 基本機能テスト実行
make test-chat     # チャット機能テスト
make test-api      # APIテスト
make test-db       # データベース接続テスト
```

### 🧹 メンテナンス・クリーンアップ

```bash
make clean         # 不要なDockerリソース削除
make clean-all     # 包括的クリーンアップ
make clean-cache   # キャッシュクリア
make clean-logs    # ログファイル削除
```

### 📈 開発支援

```bash
make shell         # アプリケーションコンテナシェル
make db-shell      # データベースコンテナシェル
make deps          # 依存関係確認
make size          # Dockerイメージサイズ確認
```

### 🚀 効率的な開発ワークフロー

```bash
# 開発開始
make dev           # 開発モード起動（ログ表示）

# 変更をテスト
make test          # 基本機能テスト
make health        # ヘルスチェック

# 問題が発生した場合
make logs          # ログ確認
make restart       # 再起動
make reset         # 完全リセット
```

## 🛠️ 従来のコマンド（参考）

Makefile を使わない場合の従来の Docker コマンドです：

```bash
# 基本操作
docker-compose up --build -d        # ビルド＆起動
docker-compose down                  # 停止＆削除
docker-compose restart              # 再起動

# ログ確認
docker-compose logs -f              # 全サービス
docker-compose logs -f chatbot      # チャットボットのみ
docker-compose logs -f postgres     # データベースのみ
docker-compose logs -f pgadmin      # pgAdminのみ

# 個別サービス制御
docker-compose up chatbot -d        # チャットボットのみ起動
docker-compose exec postgres psql -U chatbot_user -d chatbot_db  # DB接続
docker-compose exec chatbot /bin/bash  # アプリケーションシェル
```

### データベース接続

```bash
# PostgreSQLに接続
make db-connect
# または
docker-compose exec postgres psql -U chatbot_user -d chatbot_db

# テーブル確認
\dt

# 会話履歴確認
SELECT * FROM conversations ORDER BY timestamp DESC LIMIT 10;
```

### 停止・再起動

```bash
# サービス停止
docker-compose down

# 完全クリーンアップ（データも削除）
docker-compose down -v

# 再起動
docker-compose up --build
```

## 📊 データベーススキーマ

### conversations テーブル

- `id`: 主キー
- `user_id`: ユーザー ID
- `user_message`: ユーザーメッセージ
- `bot_response`: ボット応答
- `sentiment`: 感情分析結果
- `intent`: 意図分類結果
- `timestamp`: タイムスタンプ

### knowledge_base テーブル

- `id`: 主キー
- `keyword`: キーワード
- `response`: 応答文
- `confidence`: 信頼度
- `category`: カテゴリ

### intents テーブル

- `id`: 主キー
- `intent_name`: 意図名
- `patterns`: パターン配列
- `responses`: 応答配列

## 🤖 AI 機能の詳細

### 感情分析

- ポジティブ/ネガティブ単語辞書ベース
- リアルタイム感情判定
- 感情履歴の統計表示

### 意図分類

- パターンマッチングと TF-IDF
- 事前定義済み意図カテゴリ
- 学習可能な分類システム

### 応答生成

1. 意図ベース応答
2. キーワードベース応答
3. 感情配慮応答
4. デフォルト応答

## 🔧 カスタマイズ

### 新しい意図を追加

```sql
INSERT INTO intents (intent_name, patterns, responses) VALUES
('new_intent', ARRAY['パターン1', 'パターン2'], ARRAY['応答1', '応答2']);
```

### 知識ベースを拡張

```sql
INSERT INTO knowledge_base (keyword, response, category) VALUES
('新キーワード', '新しい応答', 'カテゴリ名');
```

## 🚨 トラブルシューティング

### よくある問題

1. **ポート 80 が使用中**

   ```bash
   # docker-compose.ymlの ports を変更
   ports:
     - "8080:5000"
   ```

2. **データベース接続エラー**

   ```bash
   # PostgreSQLの起動を待つ
   docker-compose logs postgres
   ```

3. **NLTK データエラー**
   ```bash
   # コンテナ内でNLTKデータをダウンロード
   docker-compose exec chatbot python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

## 📈 今後の改善計画

- [ ] より高度な自然言語処理（BERT/GPT 活用）
- [ ] 音声認識・合成機能
- [ ] 多言語対応
- [ ] REST API 提供
- [ ] ユーザー認証機能
- [ ] チャットボット学習機能の向上

## 📝 リポジトリ情報

### 🔗 リンク

- **GitHub**: https://github.com/taienobutaka/Chatbot
- **SSH Clone**: `git@github.com:taienobutaka/Chatbot.git`
- **HTTPS Clone**: `https://github.com/taienobutaka/Chatbot.git`

### 👥 コントリビューション

プルリクエストやイシューは歓迎します！以下の手順でご貢献ください：

1. このリポジトリをフォーク
2. フィーチャーブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add some amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを作成

### ⭐ サポート

このプロジェクトが役に立った場合は、ぜひ GitHub でスターをつけてください！

## 📝 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。
