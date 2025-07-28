#!/bin/bash

echo "🚀 AIチャットボット（テキスト解析機能付き）を起動しています..."

# Dockerが起動しているか確認
if ! docker info > /dev/null 2>&1; then
    echo "❌ Dockerが起動していません。Dockerを起動してください。"
    exit 1
fi

# プロジェクトディレクトリに移動
cd /home/taie/test/Python

echo "📦 コンテナをビルドしています..."
docker-compose up --build -d

echo "⏳ サービスが起動するまで待機しています..."
sleep 45

# ヘルスチェック
echo "🔍 ヘルスチェックを実行しています..."
for i in {1..10}; do
    if curl -f http://localhost/health > /dev/null 2>&1; then
        echo "✅ AIチャットボットが正常に起動しました！"
        echo ""
        echo "🌐 ブラウザで http://localhost にアクセスしてください"
        echo ""
        echo "🤖 機能:"
        echo "  - テキスト解析（感情・意図分類）"
        echo "  - インテリジェント応答生成"
        echo "  - 会話履歴管理"
        echo "  - リアルタイム分析結果表示"
        echo ""
        echo "📊 分析機能:"
        echo "  - 感情分析（positive/negative/neutral）"
        echo "  - 意図分類（greeting/goodbye/thanks等）"
        echo "  - キーワード抽出"
        echo "  - 会話統計データ"
        echo ""
        exit 0
    fi
    echo "待機中... ($i/10)"
    sleep 5
done

echo "❌ サービスの起動に失敗しました。ログを確認してください："
echo ""
echo "🔍 ログ確認コマンド:"
echo "  docker-compose logs chatbot"
echo "  docker-compose logs postgres"
echo ""
echo "🛠️ トラブルシューティング:"
echo "  docker-compose down && docker-compose up --build"
