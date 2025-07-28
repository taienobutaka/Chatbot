from flask import Flask, render_template, request, jsonify, session
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import uuid
import re
import random
import json
from datetime import datetime
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging
import sys
import pandas as pd
from textblob import TextBlob
try:
    from janome.tokenizer import Tokenizer
    JANOME_AVAILABLE = True
except ImportError:
    JANOME_AVAILABLE = False

# NLTK データダウンロード（初回のみ）
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# ログ設定を追加
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
    force=True
)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Flaskのログレベルも設定
app.logger.setLevel(logging.DEBUG)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)

class AIMessageAnalyzer:
    """テキストメッセージの解析と理解を行うクラス"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=None,  # 日本語の場合は独自に設定
            ngram_range=(1, 2)
        )
        self.japanese_stopwords = [
            'の', 'に', 'は', 'を', 'が', 'で', 'て', 'と', 'し', 'れ', 
            'さ', 'ある', 'いる', 'する', 'です', 'ます', 'だ', 'である'
        ]
    
    def preprocess_text(self, text):
        """テキストの前処理"""
        # 小文字化
        text = text.lower()
        # 特殊文字を除去
        text = re.sub(r'[^\w\s]', '', text)
        # 日本語ストップワードを除去
        words = text.split()
        words = [word for word in words if word not in self.japanese_stopwords]
        return ' '.join(words)
    
    def extract_keywords(self, text):
        """キーワード抽出"""
        processed_text = self.preprocess_text(text)
        words = processed_text.split()
        
        # 単語の頻度を計算
        word_freq = {}
        for word in words:
            if len(word) > 1:  # 1文字の単語は除外
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 頻度順にソート
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [keyword[0] for keyword in keywords[:5]]  # 上位5つのキーワード
    
    def analyze_sentiment(self, text):
        """感情分析（簡易版）"""
        positive_words = [
            '嬉しい', '楽しい', '幸せ', '良い', '素晴らしい', '最高', 
            'ありがとう', '感謝', '愛', '好き', '満足'
        ]
        negative_words = [
            '悲しい', 'つらい', '疲れた', '悪い', '嫌い', '困った', 
            '怒り', '不満', '心配', '不安', '問題'
        ]
        
        text_lower = text.lower()
        positive_score = sum(1 for word in positive_words if word in text_lower)
        negative_score = sum(1 for word in negative_words if word in text_lower)
        
        if positive_score > negative_score:
            return 'positive'
        elif negative_score > positive_score:
            return 'negative'
        else:
            return 'neutral'
    
    def classify_intent(self, text, intents_data):
        """意図分類（改善版）"""
        if not intents_data:
            return 'unknown'
        
        text_lower = text.lower()
        text_processed = self.preprocess_text(text)
        best_intent = 'unknown'
        highest_score = 0
        
        # 直接的なキーワードマッチングを優先
        for intent_data in intents_data:
            intent_name = intent_data['intent_name']
            patterns = intent_data['patterns']
            
            score = 0
            
            # 完全一致チェック（最高優先度）
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    score += 10  # 完全一致には高いスコア
            
            # 部分一致チェック
            for pattern in patterns:
                pattern_words = pattern.lower().split()
                for word in pattern_words:
                    if word in text_lower:
                        score += 2  # 部分一致には中程度のスコア
            
            # 特定の質問パターンをチェック
            if self.check_specific_patterns(text_lower, intent_name):
                score += 15  # 特定パターンには最高スコア
            
            if score > highest_score:
                highest_score = score
                best_intent = intent_name
        
        # 特別な処理：明確な質問パターンを識別
        if self.is_question_about_food(text_lower):
            return 'food'
        elif self.is_question_about_name(text_lower):
            return 'name'
        elif self.is_question_about_weather(text_lower):
            return 'weather'
        elif self.is_question_about_time(text_lower):
            return 'time'
        
        return best_intent if highest_score > 0 else 'unknown'
    
    def check_specific_patterns(self, text, intent_name):
        """特定のパターンをチェック"""
        patterns = {
            'food': ['好きな食べ物', '食べ物', '料理', '美味しい', 'グルメ'],
            'name': ['名前', '君は誰', 'あなたは', 'あなたの名前', 'ボット'],
            'weather': ['天気', '雨', '晴れ', '曇り', '雪', '降る', '降らない'],
            'time': ['時間', '今何時', '何時', '時刻'],
            'greeting': ['こんにちは', 'おはよう', 'こんばんは', 'はじめまして'],
            'goodbye': ['さようなら', 'バイバイ', 'また'],
            'thanks': ['ありがとう', 'サンキュー', '感謝']
        }
        
        if intent_name in patterns:
            return any(pattern in text for pattern in patterns[intent_name])
        
        return False
    
    def is_question_about_food(self, text):
        """食べ物に関する質問かチェック"""
        food_indicators = ['好きな食べ物', '食べ物', '料理', '何食べる', '美味しい', 'グルメ']
        return any(indicator in text for indicator in food_indicators)
    
    def is_question_about_name(self, text):
        """名前に関する質問かチェック"""
        name_indicators = ['名前', 'あなたは誰', 'あなたの名前', '君は誰', 'ボット', 'bot']
        return any(indicator in text for indicator in name_indicators)
    
    def is_question_about_weather(self, text):
        """天気に関する質問かチェック"""
        weather_indicators = ['天気', '雨', '晴れ', '曇り', '雪', '降る', '降らない']
        return any(indicator in text for indicator in weather_indicators)
    
    def is_question_about_time(self, text):
        """時間に関する質問かチェック"""
        time_indicators = ['時間', '今何時', '何時', '時刻', '今の時間']
        return any(indicator in text for indicator in time_indicators)

class ChatBot:
    def __init__(self):
        self.db_params = {
            'host': 'postgres',
            'database': 'chatbot_db',
            'user': 'chatbot_user',
            'password': 'chatbot_pass',
            'port': '5432'
        }
        self.analyzer = AIMessageAnalyzer()
        
        # 日本語トークナイザーの初期化
        self.tokenizer = None
        if JANOME_AVAILABLE:
            try:
                self.tokenizer = Tokenizer()
            except Exception as e:
                print(f"Janome初期化エラー: {e}")
        
        # 動的応答生成のための設定
        self.conversation_context = {}
        self.personality_settings = {
            'base_personality': 'friendly',
            'energy_level': 'normal',
            'formality': 'casual'
        }
    
    def get_connection(self):
        return psycopg2.connect(**self.db_params)
    
    def save_conversation(self, user_id, user_message, bot_response, session_id, sentiment=None, intent=None):
        print(f"🔍 DEBUG: Attempting to save conversation")
        print(f"   User ID: {user_id}")
        print(f"   Message: {user_message}")
        print(f"   Response: {bot_response}")
        print(f"   Session: {session_id}")
        print(f"   Sentiment: {sentiment}")
        print(f"   Intent: {intent}")
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO conversations (user_id, user_message, bot_response, session_id, sentiment, intent)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (user_id, user_message, bot_response, session_id, sentiment, intent))
                
                result = cursor.fetchone()
                conn.commit()
                print(f"✅ SUCCESS: Conversation saved with ID: {result[0]}")
                return result[0]
                
        except Exception as e:
            print(f"❌ ERROR: Failed to save conversation: {e}")
            import traceback
            print(traceback.format_exc())
            raise
    
    def get_intents_data(self):
        """インテントデータを取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("SELECT intent_name, patterns, responses FROM intents")
                return cursor.fetchall()
        except Exception as e:
            print(f"インテントデータ取得エラー: {e}")
            return []
    
    def get_response_by_intent(self, intent, user_message="", sentiment="neutral"):
        """インテントに基づいて応答を取得（コンテキスト考慮）"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("SELECT responses FROM intents WHERE intent_name = %s", (intent,))
                result = cursor.fetchone()
                
                if result and result['responses']:
                    base_response = random.choice(result['responses'])
                    
                    # 時間に基づく応答の調整
                    enhanced_response = self.enhance_response_with_context(
                        base_response, intent, sentiment, user_message
                    )
                    
                    return enhanced_response
        except Exception as e:
            print(f"インテント応答取得エラー: {e}")
        
        return None
    
    def enhance_response_with_context(self, base_response, intent, sentiment, user_message=""):
        """コンテキストを考慮した応答の強化"""
        current_hour = datetime.now().hour
        
        # 時間帯による調整
        time_modifiers = self.get_time_based_modifiers(current_hour)
        
        # 感情に基づく調整
        emotion_modifiers = self.get_emotion_based_modifiers(sentiment)
        
        # ランダムな感嘆符や文末詞の追加
        filler_expressions = self.get_conversation_fillers()
        
        # 応答の強化
        enhanced = base_response
        
        # 時間帯の挨拶を追加（greeting インテントの場合）
        if intent == 'greeting' and time_modifiers:
            enhanced = f"{time_modifiers['greeting']} {enhanced}"
        
        # 感情に応じた修飾語を追加
        if emotion_modifiers and random.random() < 0.3:  # 30%の確率で追加
            enhanced = f"{enhanced} {emotion_modifiers}"
        
        # 会話を活発にするためのフィラー表現
        if filler_expressions and random.random() < 0.2:  # 20%の確率で追加
            enhanced = f"{enhanced} {filler_expressions}"
        
        return enhanced
    
    def get_time_based_modifiers(self, hour):
        """時間帯に基づく修飾表現"""
        if 5 <= hour < 10:
            return {
                'greeting': '朝の清々しい時間ですね！',
                'energy': 'high',
                'tone': 'energetic'
            }
        elif 10 <= hour < 12:
            return {
                'greeting': '午前中の爽やかな時間ですね！',
                'energy': 'high',
                'tone': 'active'
            }
        elif 12 <= hour < 14:
            return {
                'greeting': 'お昼の時間ですね！',
                'energy': 'normal',
                'tone': 'relaxed'
            }
        elif 14 <= hour < 17:
            return {
                'greeting': '午後のひととき、いかがお過ごしですか？',
                'energy': 'normal',
                'tone': 'calm'
            }
        elif 17 <= hour < 19:
            return {
                'greeting': '夕方の時間ですね。お疲れさまです！',
                'energy': 'low',
                'tone': 'supportive'
            }
        elif 19 <= hour < 22:
            return {
                'greeting': '夜の時間、ゆっくりされていますか？',
                'energy': 'low',
                'tone': 'gentle'
            }
        else:
            return {
                'greeting': '夜更かしですね！',
                'energy': 'low',
                'tone': 'caring'
            }
    
    def get_emotion_based_modifiers(self, sentiment):
        """感情に基づく修飾表現"""
        emotion_responses = {
            'positive': [
                '本当に素敵ですね！', 'わくわくしますね！', 'とても良いことですね！',
                'すごく嬉しいです！', 'それは最高ですね！'
            ],
            'negative': [
                'お気持ちお察しします。', 'そんな時もありますよね。', 'お疲れさまです。',
                '一緒に考えさせてください。', '無理しないでくださいね。'
            ],
            'neutral': [
                'なるほどですね。', 'そうなんですね。', '興味深いお話ですね。',
                'よくわかります。', 'そうですね。'
            ]
        }
        
        if sentiment in emotion_responses:
            return random.choice(emotion_responses[sentiment])
        
        return random.choice(emotion_responses['neutral'])
    
    def get_conversation_fillers(self):
        """会話を豊かにするフィラー表現"""
        fillers = [
            'ところで、', 'それにしても、', 'そういえば、', 'ちなみに、',
            'もしよろしければ、', 'お時間があるときに、', 'もしかして、',
            'いかがでしょうか？', 'どう思われますか？', 'よろしければまた教えてくださいね。'
        ]
        
        return random.choice(fillers) if random.random() < 0.5 else ""
    
    def analyze_conversation_pattern(self, user_id):
        """ユーザーの会話パターンを分析"""
        try:
            history = self.get_conversation_history(user_id, limit=20)
            if not history:
                return {}
            
            # 感情パターンの分析
            sentiments = [conv['sentiment'] for conv in history if conv['sentiment']]
            
            # 頻出インテントの分析
            intents = [conv['intent'] for conv in history if conv['intent']]
            
            # 会話時間帯の分析
            timestamps = [conv['timestamp'] for conv in history]
            hours = [ts.hour for ts in timestamps]
            
            pattern = {
                'dominant_sentiment': max(set(sentiments), key=sentiments.count) if sentiments else 'neutral',
                'frequent_intents': list(set(intents))[:3] if intents else [],
                'active_hours': list(set(hours))[:3] if hours else [],
                'conversation_count': len(history)
            }
            
            return pattern
            
        except Exception as e:
            print(f"会話パターン分析エラー: {e}")
            return {}
    
    def get_response_by_keyword(self, keywords):
        """キーワードに基づいて応答を取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                for keyword in keywords:
                    cursor.execute("""
                        SELECT response FROM knowledge_base 
                        WHERE keyword ILIKE %s 
                        ORDER BY confidence DESC 
                        LIMIT 1
                    """, (f'%{keyword}%',))
                    
                    result = cursor.fetchone()
                    if result:
                        return result['response']
        except Exception as e:
            print(f"キーワード応答取得エラー: {e}")
        
        return None
    
    def get_response(self, user_message, user_id=None):
        """シンプルで正確な応答生成"""
        # テキスト解析
        keywords = self.analyzer.extract_keywords(user_message)
        sentiment = self.analyzer.analyze_sentiment(user_message)
        
        # インテント分類
        intents_data = self.get_intents_data()
        intent = self.analyzer.classify_intent(user_message, intents_data)
        
        print(f"分析結果 - メッセージ: '{user_message}', キーワード: {keywords}, 感情: {sentiment}, 意図: {intent}")
        
        # 応答生成の優先順位
        # 1. 明確にマッチしたインテントベースの応答
        if intent != 'unknown':
            response = self.get_simple_response_by_intent(intent)
            if response:
                print(f"インテント応答: {response}")
                return response, sentiment, intent
        
        # 2. キーワードベースの応答
        response = self.get_response_by_keyword(keywords)
        if response:
            print(f"キーワード応答: {response}")
            return response, sentiment, intent
        
        # 3. 感情に基づくシンプルな応答
        if sentiment == 'positive':
            response = "それは素晴らしいですね！"
        elif sentiment == 'negative':
            response = "大変でしたね。お疲れさまです。"
        else:
            # 4. デフォルト応答
            response = "なるほど、そうなんですね。もう少し詳しく教えてください。"
        
        print(f"デフォルト応答: {response}")
        return response, sentiment, intent
    
    def get_simple_response_by_intent(self, intent):
        """インテントに基づくシンプルな応答"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("SELECT responses FROM intents WHERE intent_name = %s", (intent,))
                result = cursor.fetchone()
                
                if result and result['responses']:
                    # ランダムに1つ選択（コンテキスト強化なし）
                    return random.choice(result['responses'])
        except Exception as e:
            print(f"インテント応答取得エラー: {e}")
        
        return None
    
    def generate_emotion_based_response(self, sentiment, user_message, conversation_pattern):
        """感情に基づく動的応答生成"""
        time_context = self.get_time_based_modifiers(datetime.now().hour)
        
        if sentiment == 'positive':
            positive_responses = [
                f"それは{time_context.get('tone', '素晴らしい')}ですね！一緒に喜ばせてもらいます！",
                "とても良いニュースですね。私も嬉しくなります！",
                "ポジティブなエネルギーが伝わってきます！",
                "そんな風に感じられるなんて、とても素敵なことですね。",
                "明るい気持ちになれる話をありがとうございます！"
            ]
            
            # 会話パターンに基づく調整
            if conversation_pattern.get('dominant_sentiment') == 'positive':
                positive_responses.extend([
                    "いつも前向きで素敵ですね！",
                    "あなたのポジティブさに元気をもらいます！"
                ])
            
            return random.choice(positive_responses)
            
        elif sentiment == 'negative':
            negative_responses = [
                f"それは大変でしたね。{time_context.get('tone', 'お疲れさまです')}。",
                "つらい気持ち、よく分かります。一人で抱え込まずに話してくださいね。",
                "そんな時もありますよね。無理しないでくださいね。",
                "何かお手伝いできることがあれば、遠慮なく言ってください。",
                "お疲れさまです。少しでも気持ちが楽になればいいのですが。"
            ]
            
            # 時間帯による調整
            if datetime.now().hour >= 19:  # 夜の時間
                negative_responses.extend([
                    "夜の時間は気持ちも沈みがちですよね。ゆっくり休んでください。",
                    "一日お疲れさまでした。明日はきっと良い日になりますよ。"
                ])
            
            return random.choice(negative_responses)
        
        return None
    
    def generate_personalized_default_response(self, user_message, conversation_pattern):
        """パーソナライズされたデフォルト応答"""
        base_responses = [
            "それは興味深いですね。もう少し詳しく教えてください。",
            "なるほど、そうなんですね。",
            "わかりました。他に何かありますか？",
            "そのことについてもっと知りたいです。",
            "とても面白い話ですね。",
            "そうですね。どう思われますか？",
            "それについてどう感じていますか？"
        ]
        
        # 頻出インテントに基づく調整
        frequent_intents = conversation_pattern.get('frequent_intents', [])
        if 'hobby' in frequent_intents:
            base_responses.extend([
                "それも趣味の一つですか？",
                "新しい発見ですね！",
                "興味のあることは尽きませんね。"
            ])
        
        if 'emotion_positive' in frequent_intents:
            base_responses.extend([
                "いつも楽しそうで素敵ですね！",
                "ポジティブなお話、もっと聞かせてください。"
            ])
        
        # 会話回数に基づく親しみやすさの調整
        conversation_count = conversation_pattern.get('conversation_count', 0)
        if conversation_count > 10:
            base_responses.extend([
                "いつもお話しできて嬉しいです！",
                "また今日もお会いできて良かったです。",
                "最近いかがお過ごしですか？"
            ])
        
        return random.choice(base_responses)
    
    def apply_personality_adjustments(self, response, conversation_pattern):
        """パーソナリティに基づく応答調整"""
        # 感情的トーンの調整
        dominant_sentiment = conversation_pattern.get('dominant_sentiment', 'neutral')
        
        if dominant_sentiment == 'positive':
            # より明るく、エネルギッシュに
            if not any(char in response for char in ['！', '!', '♪', '✨']):
                if random.random() < 0.4:
                    response += '✨'
        
        elif dominant_sentiment == 'negative':
            # より穏やかで支援的に
            supportive_endings = [' お気軽にお話しくださいね。', ' 一緒に考えさせてください。', ' 応援しています。']
            if random.random() < 0.3:
                response += random.choice(supportive_endings)
        
        return response
    
    def get_conversation_history(self, user_id, limit=10):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT user_message, bot_response, timestamp, sentiment, intent
                    FROM conversations 
                    WHERE user_id = %s 
                    ORDER BY timestamp DESC 
                    LIMIT %s
                """, (user_id, limit))
                
                return cursor.fetchall()
        except Exception as e:
            print(f"履歴取得エラー: {e}")
            return []
    
    def get_analytics(self, user_id):
        """ユーザーの会話分析データを取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                # 感情分析
                cursor.execute("""
                    SELECT sentiment, COUNT(*) as count
                    FROM conversations 
                    WHERE user_id = %s AND sentiment IS NOT NULL
                    GROUP BY sentiment
                """, (user_id,))
                sentiment_data = cursor.fetchall()
                
                # インテント分析
                cursor.execute("""
                    SELECT intent, COUNT(*) as count
                    FROM conversations 
                    WHERE user_id = %s AND intent IS NOT NULL
                    GROUP BY intent
                    ORDER BY count DESC
                    LIMIT 5
                """, (user_id,))
                intent_data = cursor.fetchall()
                
                return {
                    'sentiment_analysis': sentiment_data,
                    'top_intents': intent_data
                }
        except Exception as e:
            print(f"分析データ取得エラー: {e}")
            return {'sentiment_analysis': [], 'top_intents': []}

# チャットボットインスタンス
chatbot = ChatBot()

@app.route('/')
def index():
    # セッションIDを生成
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    if 'user_id' not in session:
        session['user_id'] = f"user_{uuid.uuid4().hex[:8]}"
    
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'メッセージが空です'}), 400
        
        # ユーザーIDを取得
        user_id = session.get('user_id', 'anonymous_user')
        session_id = session.get('session_id', 'default_session')
        
        # AI分析とボットの応答を取得（ユーザーIDを含む）
        bot_response, sentiment, intent = chatbot.get_response(user_message, user_id)
        
        print(f"保存データ: user_id={user_id}, message='{user_message}', response='{bot_response}', sentiment={sentiment}, intent={intent}")
        
        # 会話を保存
        chatbot.save_conversation(user_id, user_message, bot_response, session_id, sentiment, intent)
        
        return jsonify({
            'response': bot_response,
            'sentiment': sentiment,
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"チャットエラー: {e}")
        return jsonify({'error': 'サーバーエラーが発生しました'}), 500

@app.route('/history')
def history():
    try:
        user_id = session.get('user_id')
        conversations = chatbot.get_conversation_history(user_id)
        
        return jsonify({
            'conversations': [
                {
                    'user_message': conv['user_message'],
                    'bot_response': conv['bot_response'],
                    'sentiment': conv['sentiment'],
                    'intent': conv['intent'],
                    'timestamp': conv['timestamp'].isoformat()
                } for conv in conversations
            ]
        })
        
    except Exception as e:
        print(f"履歴取得エラー: {e}")
        return jsonify({'error': '履歴の取得に失敗しました'}), 500

@app.route('/analytics')
def analytics():
    try:
        user_id = session.get('user_id')
        analytics_data = chatbot.get_analytics(user_id)
        
        return jsonify(analytics_data)
        
    except Exception as e:
        print(f"分析データ取得エラー: {e}")
        return jsonify({'error': '分析データの取得に失敗しました'}), 500

@app.route('/health')
def health():
    try:
        with chatbot.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
