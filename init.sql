-- データベース初期化スクリプト

-- 会話履歴テーブル
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(255),
    sentiment VARCHAR(20),
    intent VARCHAR(100)
);

-- 知識ベーステーブル
CREATE TABLE IF NOT EXISTS knowledge_base (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL,
    response TEXT NOT NULL,
    confidence REAL DEFAULT 1.0,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ユーザー情報テーブル
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    preferences JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- インテントテーブル（意図分類用）
CREATE TABLE IF NOT EXISTS intents (
    id SERIAL PRIMARY KEY,
    intent_name VARCHAR(100) NOT NULL,
    patterns TEXT[] NOT NULL,
    responses TEXT[] NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- インデックス作成
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
CREATE INDEX IF NOT EXISTS idx_knowledge_keyword ON knowledge_base(keyword);
CREATE INDEX IF NOT EXISTS idx_intents_name ON intents(intent_name);

-- 初期データ挿入
INSERT INTO knowledge_base (keyword, response, category) VALUES
('こんにちは', 'こんにちは！元気ですか？', 'greeting'),
('はじめまして', 'はじめまして！よろしくお願いします。', 'greeting'),
('おはよう', 'おはようございます！今日もいい一日にしましょう。', 'greeting'),
('こんばんは', 'こんばんは！お疲れさまです。', 'greeting'),
('ありがとう', 'どういたしまして！お役に立てて嬉しいです。', 'thanks'),
('名前', '私はAIチャットボットです。なんでも聞いてください！', 'about'),
('天気', '天気予報は外部のサービスで確認してくださいね。', 'weather'),
('さようなら', 'さようなら！また話しましょう。', 'goodbye'),
('バイバイ', 'バイバイ！また会いましょう。', 'goodbye'),
('元気', '私は元気です！ありがとうございます。あなたはいかがですか？', 'greeting'),
('疲れた', 'お疲れさまです。ゆっくり休んでくださいね。', 'sympathy'),
('嬉しい', 'それは良かったです！一緒に喜ばせてもらいます。', 'emotion'),
('悲しい', '大丈夫ですか？何かお手伝いできることがあれば言ってください。', 'emotion')
ON CONFLICT DO NOTHING;

-- インテントデータ挿入
INSERT INTO intents (intent_name, patterns, responses) VALUES
('greeting', ARRAY['こんにちは', 'はじめまして', 'おはよう', 'こんばんは', 'やあ', 'ハロー', 'お疲れ様', 'どうも'], 
 ARRAY[
   'こんにちは！今日は何か面白いことありましたか？',
   'はじめまして！何でも気軽に話しかけてくださいね。',
   'お疲れさまです！今日はどんな一日でしたか？',
   'やあ！調子はどうですか？',
   'どうも！何か楽しい話でもしませんか？',
   'こんにちは！今日は素敵な一日になりそうですね。',
   'お元気ですか？何かお手伝いできることがあれば言ってくださいね！',
   'おはようございます！今日も一日頑張りましょう！',
   '朝の清々しい時間ですね。コーヒーはもう飲まれましたか？'
 ]),
('goodbye', ARRAY['さようなら', 'バイバイ', 'また', 'おつかれ', 'さらば', 'お疲れ', 'またね'], 
 ARRAY[
   'さようなら！また話しましょう！',
   'また会いましょう！素敵な時間をお過ごしください。',
   'お疲れさまでした！今日も一日お疲れさまでした。',
   'またお話しできるのを楽しみにしています！',
   'バイバイ！何かあったらいつでも話しかけてくださいね。',
   '良い一日をお過ごしください！',
   'またいつでもお気軽にどうぞ！'
 ]),
('thanks', ARRAY['ありがとう', '感謝', 'サンキュー', 'thx', 'どうも', 'おつかれ'], 
 ARRAY[
   'どういたしまして！お役に立てて嬉しいです！',
   'こちらこそ、楽しい会話をありがとうございます！',
   'いつでもどうぞ！何かお手伝いできることがあれば言ってくださいね。',
   'お役に立てて光栄です！また何かありましたらお声かけください。',
   'ありがとうございます！そう言っていただけると嬉しいです。',
   'とんでもないです！いつでもお気軽にどうぞ。'
 ]),
('name', ARRAY['名前', '君は誰', 'あなたは', 'bot', 'ボット', 'あなたの名前'], 
 ARRAY[
   '私はAIチャットボットです！何でも気軽に話しかけてください。',
   'チャットボットと呼んでください。皆さんとお話しするのが大好きです！',
   'AIアシスタントです。会話を通じてお手伝いできることを探しています。',
   '私は会話を楽しむAIチャットボットです。あなたのことも教えてください！',
   'チャットボットという名前で活動しています。よろしくお願いします！'
 ]),
('weather', ARRAY['天気', '気温', '雨', '晴れ', '曇り', '雪', '暑い', '寒い', '湿度', '降る', '降らない'], 
 ARRAY[
   '今日の天気はどうですか？外の様子を教えてください！',
   '天気予報をチェックしてみてはいかがでしょう？',
   'いい天気だと気分も上がりますよね！',
   '雨の日は読書や映画鑑賞にぴったりですね。',
   '暑い日は水分補給を忘れずに！',
   '寒い日は温かい飲み物でほっこりしませんか？',
   '季節の変わり目は体調管理に気をつけてくださいね。',
   '外を見てみましょう！どんな空模様ですか？'
 ]),
('time', ARRAY['時間', '今何時', '何時', '時刻', '今の時間'], 
 ARRAY[
   '申し訳ありませんが、正確な時刻をお伝えできません。お使いのデバイスでご確認ください。',
   '時計をご覧になってみてください。今は何時でしょうか？',
   '時間の感覚は人それぞれですね。今はどんな時間帯ですか？',
   'お時間を気にされているのですね。何か予定がありますか？',
   '時間について気になることがあれば、お聞かせください。'
 ]),
('food', ARRAY['食べ物', '料理', '美味しい', 'グルメ', 'レストラン', 'カフェ', '飲み物', '食事', '好きな食べ物'], 
 ARRAY[
   'どんな食べ物がお好きですか？私もいろいろな料理の話を聞くのが大好きです！',
   '美味しそうですね！どんな味でしたか？',
   'グルメな話は聞いているだけでお腹が空いてきます！',
   '新しいお店を開拓するのは楽しいですよね。',
   'その料理、作り方を覚えてみたいですね！',
   '食事は人生の楽しみの一つですよね。',
   'カフェでゆっくりする時間は贅沢ですね。',
   '美味しい食べ物の話、もっと聞かせてください！'
 ]),
('emotion_positive', ARRAY['嬉しい', '楽しい', '幸せ', 'ハッピー', '最高', '素晴らしい', '良い'], 
 ARRAY[
   'それは素晴らしいですね！一緒に喜ばせてもらいます！',
   'とても良いニュースですね。私も嬉しくなります！',
   'ポジティブなエネルギーが伝わってきます！',
   'そんな風に感じられるなんて、とても幸せなことですね。',
   '明るい気持ちになれる話をありがとうございます！',
   'そのお気持ち、とてもよく分かります！',
   '素敵な体験をされたんですね！'
 ]),
('emotion_negative', ARRAY['悲しい', 'つらい', '疲れた', '大変', '困った', '辛い', '不安'], 
 ARRAY[
   'それは大変でしたね。お疲れさまです。',
   'つらい気持ち、よく分かります。',
   'そんな時もありますよね。無理しないでくださいね。',
   '何かお手伝いできることがあれば、遠慮なく言ってください。',
   'ゆっくり休んで、また明日から頑張りましょう。',
   '大丈夫ですか？少しでも気持ちが楽になればいいのですが。',
   'お疲れさまです。一人で抱え込まずに、話してくださいね。'
 ]),
('hobby', ARRAY['趣味', '好き', '興味', '楽しい', '映画', '音楽', '読書', 'ゲーム', 'スポーツ'], 
 ARRAY[
   'それは素敵な趣味ですね！詳しく教えてください。',
   '私も興味があります！どんなところが魅力的ですか？',
   '楽しそうですね！始めたきっかけはありますか？',
   'その分野のおすすめがあったら教えてください！',
   '新しいことを学ぶのは刺激的ですよね。',
   '趣味の時間は大切ですよね。リフレッシュできそうです！',
   'そのご趣味、とても興味深いです！'
 ])
ON CONFLICT (intent_name) DO UPDATE SET
patterns = EXCLUDED.patterns,
responses = EXCLUDED.responses;
