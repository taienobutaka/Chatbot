# AI チャットボット - 効率的な開発・運用のためのMakefile

.PHONY: help install build up down restart logs clean test dev prod status health reset

# デフォルトターゲット
.DEFAULT_GOAL := help

# 色付きヘルプメッセージ
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

## 基本操作

help: ## このヘルプメッセージを表示
	@echo ""
	@echo "$(CYAN)AI チャットボット - Makefile コマンド$(RESET)"
	@echo ""
	@echo "$(GREEN)基本操作:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)使用例:$(RESET)"
	@echo "  make start     # 環境構築から起動まで一括実行"
	@echo "  make dev       # 開発モードで起動"
	@echo "  make reset     # 完全リセット & 再構築"
	@echo ""

## 環境構築・起動

start: ## 🚀 環境構築から起動まで一括実行（初回・推奨）
	@echo "$(GREEN)🚀 AI チャットボット環境を構築・起動中...$(RESET)"
	@make build
	@make up
	@make status
	@echo ""
	@echo "$(GREEN)✅ 起動完了！$(RESET)"
	@echo "$(CYAN)📱 チャットボット: http://localhost$(RESET)"
	@echo "$(CYAN)🗄️  pgAdmin: http://localhost:8080$(RESET)"
	@echo ""

build: ## 🔨 Dockerイメージをビルド
	@echo "$(YELLOW)🔨 Dockerイメージをビルド中...$(RESET)"
	docker-compose build --no-cache

up: ## ⬆️ サービスを起動（バックグラウンド）
	@echo "$(YELLOW)⬆️ サービスを起動中...$(RESET)"
	docker-compose up -d

dev: ## 🛠️ 開発モードで起動（ログ表示）
	@echo "$(YELLOW)🛠️ 開発モードで起動中（Ctrl+Cで停止）...$(RESET)"
	docker-compose up

## 運用・メンテナンス

stop: ## ⏹️ サービスを停止
	@echo "$(YELLOW)⏹️ サービスを停止中...$(RESET)"
	docker-compose stop

down: ## ⬇️ サービスを停止・削除
	@echo "$(YELLOW)⬇️ サービスを停止・削除中...$(RESET)"
	docker-compose down

restart: ## 🔄 サービスを再起動
	@echo "$(YELLOW)🔄 サービスを再起動中...$(RESET)"
	docker-compose restart

## ログ・監視

logs: ## 📋 全サービスのログを表示
	docker-compose logs -f

logs-chatbot: ## 🤖 チャットボットのログのみ表示
	docker-compose logs -f chatbot

logs-db: ## 🗄️ データベースのログのみ表示
	docker-compose logs -f postgres

status: ## 📊 サービスの状態を確認
	@echo "$(CYAN)📊 サービス状態:$(RESET)"
	@docker-compose ps
	@echo ""
	@echo "$(CYAN)💾 Docker ボリューム:$(RESET)"
	@docker volume ls | grep python || echo "  なし"
	@echo ""

health: ## 🏥 ヘルスチェック
	@echo "$(CYAN)🏥 ヘルスチェック実行中...$(RESET)"
	@curl -s http://localhost/health | grep -q "healthy" && echo "$(GREEN)✅ チャットボット: 正常$(RESET)" || echo "$(RED)❌ チャットボット: 異常$(RESET)"
	@echo ""

## データベース操作

db-connect: ## 🔗 データベースに接続
	@echo "$(YELLOW)🔗 PostgreSQLに接続中...$(RESET)"
	docker-compose exec postgres psql -U chatbot_user -d chatbot_db

db-backup: ## 💾 データベースをバックアップ
	@echo "$(YELLOW)💾 データベースをバックアップ中...$(RESET)"
	@mkdir -p backups
	docker-compose exec postgres pg_dump -U chatbot_user chatbot_db > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ バックアップ完了: backups/backup_$(shell date +%Y%m%d_%H%M%S).sql$(RESET)"

db-reset: ## 🗑️ データベースをリセット
	@echo "$(RED)⚠️  データベースをリセットします。続行しますか？ [y/N]$(RESET)" && read ans && [ $${ans:-N} = y ]
	@make down
	docker volume rm python_postgres_data || true
	@make up
	@echo "$(GREEN)✅ データベースリセット完了$(RESET)"

## クリーンアップ・リセット

clean: ## 🧹 不要なDockerリソースを削除
	@echo "$(YELLOW)🧹 不要なDockerリソースを削除中...$(RESET)"
	docker system prune -f
	docker volume prune -f

reset: ## 🔄 完全リセット & 再構築
	@echo "$(RED)⚠️  システムを完全リセットします。続行しますか？ [y/N]$(RESET)" && read ans && [ $${ans:-N} = y ]
	@make down
	docker volume rm python_postgres_data || true
	docker system prune -f
	@make build
	@make up
	@make status
	@echo "$(GREEN)✅ 完全リセット完了！$(RESET)"

## テスト・デバッグ

test: ## 🧪 基本的な機能テスト
	@echo "$(YELLOW)🧪 基本機能テスト実行中...$(RESET)"
	@echo "📝 好きな食べ物は:"
	@curl -s -X POST http://localhost/chat -H "Content-Type: application/json" -d '{"message": "好きな食べ物は"}' | python3 -c "import sys, json; print('  応答:', json.load(sys.stdin)['response'])"
	@echo "📝 あなたの名前は:"
	@curl -s -X POST http://localhost/chat -H "Content-Type: application/json" -d '{"message": "あなたの名前は"}' | python3 -c "import sys, json; print('  応答:', json.load(sys.stdin)['response'])"
	@echo "📝 今の時間は:"
	@curl -s -X POST http://localhost/chat -H "Content-Type: application/json" -d '{"message": "今の時間は"}' | python3 -c "import sys, json; print('  応答:', json.load(sys.stdin)['response'])"
	@echo "$(GREEN)✅ テスト完了$(RESET)"

debug: ## 🐛 デバッグ情報を表示
	@echo "$(CYAN)🐛 デバッグ情報:$(RESET)"
	@echo "Docker バージョン:"
	@docker --version
	@echo ""
	@echo "Docker Compose バージョン:"
	@docker-compose --version
	@echo ""
	@echo "利用可能なポート:"
	@ss -tlnp | grep -E ':(80|5432|8080)' || echo "  関連ポートは使用されていません"
	@echo ""

## 便利なショートカット

open: ## 🌐 ブラウザでアプリを開く
	@echo "$(CYAN)🌐 ブラウザでアプリを開きます...$(RESET)"
	@which xdg-open > /dev/null && xdg-open http://localhost || \
	which open > /dev/null && open http://localhost || \
	echo "$(YELLOW)手動でブラウザから http://localhost にアクセスしてください$(RESET)"

open-pgadmin: ## 🗄️ pgAdminを開く
	@echo "$(CYAN)🗄️ pgAdminを開きます...$(RESET)"
	@which xdg-open > /dev/null && xdg-open http://localhost:8080 || \
	which open > /dev/null && open http://localhost:8080 || \
	echo "$(YELLOW)手動でブラウザから http://localhost:8080 にアクセスしてください$(RESET)"

install: ## 📦 必要な依存関係をインストール（Docker/Docker Compose）
	@echo "$(YELLOW)📦 依存関係チェック中...$(RESET)"
	@which docker > /dev/null || (echo "$(RED)❌ Dockerがインストールされていません$(RESET)" && exit 1)
	@which docker-compose > /dev/null || (echo "$(RED)❌ Docker Composeがインストールされていません$(RESET)" && exit 1)
	@echo "$(GREEN)✅ 依存関係OK$(RESET)"

## 情報表示

info: ## ℹ️ プロジェクト情報を表示
	@echo "$(CYAN)ℹ️  AI チャットボット プロジェクト情報$(RESET)"
	@echo ""
	@echo "📁 プロジェクトディレクトリ: $(PWD)"
	@echo "🐳 Docker Compose ファイル: docker-compose.yml"
	@echo "🌐 チャットボット URL: http://localhost"
	@echo "🗄️  pgAdmin URL: http://localhost:8080"
	@echo "🗃️  データベース: PostgreSQL 15"
	@echo "🐍 Python: 3.11"
	@echo "⚡ Flask: 開発サーバー"
	@echo ""
	@echo "$(GREEN)📚 利用可能なコマンド: make help$(RESET)"
