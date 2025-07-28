# AI チャットボット - テキスト解析機能付き

Python で開発されたシンプルな AI チャットボットです。テキストメッセージの解析と理解機能を備えています。

## 🚀 機能

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

- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Frontend**: HTML/CSS/JavaScript
- **Container**: Docker & Docker Compose
- **AI/ML**: NLTK, scikit-learn
- **Text Analysis**: TF-IDF, Cosine Similarity

## 📁 プロジェクト構造

```
Python/
├── app.py                 # メインアプリケーション
├── docker-compose.yml    # Docker Compose設定
├── Dockerfile            # Docker設定
├── requirements.txt      # Python依存関係
├── init.sql             # データベース初期化
├── start.sh             # 起動スクリプト
├── templates/
│   └── chat.html        # HTMLテンプレート
├── static/
│   ├── css/
│   │   └── style.css    # スタイルシート
│   └── js/
│       └── chat.js      # JavaScript
└── README.md            # このファイル
```

## 🚀 起動方法

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

## 🌐 アクセス

起動後、以下の URL にアクセス:

- **メインアプリ**: http://localhost
- **ヘルスチェック**: http://localhost/health
- **PostgreSQL 管理 (pgAdmin)**: http://localhost:8080

### pgAdmin ログイン情報

- **メールアドレス**: admin@admin.com
- **パスワード**: admin

### PostgreSQL 接続設定（pgAdmin 内）

- **ホスト名**: postgres
- **ポート**: 5432
- **データベース名**: chatbot_db
- **ユーザー名**: chatbot_user
- **パスワード**: chatbot_pass

## 🔧 開発・デバッグ

### ログ確認

```bash
# アプリケーションログ
docker-compose logs -f chatbot

# データベースログ
docker-compose logs -f postgres

# 全サービスのログ
docker-compose logs -f
```

### データベース接続

```bash
# PostgreSQLに接続
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

## 📝 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

## 🤝 貢献

プルリクエストや問題報告を歓迎します。

---

**開発者**: AI チャットボット開発チーム  
**バージョン**: 1.0.0  
**最終更新**: 2025 年 7 月 28 日
# Chatbot
