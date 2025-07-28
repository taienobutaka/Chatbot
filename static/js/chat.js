document.addEventListener("DOMContentLoaded", function () {
  const messageInput = document.getElementById("messageInput");
  const sendButton = document.getElementById("sendButton");
  const chatMessages = document.getElementById("chatMessages");
  const loadingIndicator = document.getElementById("loadingIndicator");

  // Enterキーでメッセージ送信
  messageInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // 初期フォーカス
  messageInput.focus();

  // 初期状態でステータスインジケーターを更新
  updateStatusIndicators("neutral", "unknown");
});

async function sendMessage() {
  const messageInput = document.getElementById("messageInput");
  const message = messageInput.value.trim();

  if (!message) return;

  // ユーザーメッセージを表示
  addMessage("user", message);
  messageInput.value = "";

  // 送信ボタンを無効化
  const sendButton = document.getElementById("sendButton");
  sendButton.disabled = true;

  // ローディング表示
  showLoading(true);

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });

    const data = await response.json();

    if (response.ok) {
      // ボットの応答を表示（分析情報付き）
      addMessage("bot", data.response, {
        sentiment: data.sentiment,
        intent: data.intent,
      });

      // ステータスインジケーターを更新
      updateStatusIndicators(data.sentiment, data.intent);
    } else {
      addMessage(
        "bot",
        "エラーが発生しました: " + (data.error || "不明なエラー")
      );
    }
  } catch (error) {
    console.error("Error:", error);
    addMessage(
      "bot",
      "ネットワークエラーが発生しました。しばらく待ってから再試行してください。"
    );
  }

  // ローディング非表示
  showLoading(false);

  // 送信ボタンを有効化
  sendButton.disabled = false;
  messageInput.focus();
}

function addMessage(sender, text, analysis = null) {
  const chatMessages = document.getElementById("chatMessages");
  const messageDiv = document.createElement("div");
  const currentTime = new Date().toLocaleTimeString("ja-JP", {
    hour: "2-digit",
    minute: "2-digit",
  });

  messageDiv.className = `message ${sender}-message`;

  let analysisHtml = "";
  if (analysis && sender === "bot") {
    const sentimentEmoji = getSentimentEmoji(analysis.sentiment);
    const intentLabel = getIntentLabel(analysis.intent);

    analysisHtml = `
            <div class="message-analysis">
                ${sentimentEmoji} 感情: ${analysis.sentiment} | 🎯 意図: ${intentLabel}
            </div>
        `;
  }

  messageDiv.innerHTML = `
        <div class="message-content">
            <strong>${
              sender === "user" ? "あなた" : "ボット"
            }:</strong> ${escapeHtml(text)}
        </div>
        ${analysisHtml}
        <div class="message-time">${currentTime}</div>
    `;

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function updateStatusIndicators(sentiment, intent) {
  const sentimentIndicator = document.getElementById("sentimentIndicator");
  const intentIndicator = document.getElementById("intentIndicator");

  // 感情インジケーター
  sentimentIndicator.textContent = sentiment || "-";
  sentimentIndicator.className = `status-value sentiment-${
    sentiment || "neutral"
  }`;

  // 意図インジケーター
  intentIndicator.textContent = getIntentLabel(intent) || "-";
}

function getSentimentEmoji(sentiment) {
  const emojiMap = {
    positive: "😊",
    negative: "😔",
    neutral: "😐",
  };
  return emojiMap[sentiment] || "🤖";
}

function getIntentLabel(intent) {
  const labelMap = {
    greeting: "挨拶",
    goodbye: "別れ",
    thanks: "感謝",
    name: "名前",
    weather: "天気",
    emotion_positive: "ポジティブ",
    emotion_negative: "ネガティブ",
    unknown: "不明",
  };
  return labelMap[intent] || intent;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function showLoading(show) {
  const loadingIndicator = document.getElementById("loadingIndicator");
  loadingIndicator.style.display = show ? "block" : "none";
}

function clearChat() {
  const chatMessages = document.getElementById("chatMessages");
  chatMessages.innerHTML = `
        <div class="message bot-message">
            <div class="message-content">
                <strong>ボット:</strong> チャットがクリアされました。何でも聞いてください！
            </div>
            <div class="message-time"></div>
        </div>
    `;

  // ステータスインジケーターをリセット
  updateStatusIndicators("neutral", "unknown");
}

async function loadHistory() {
  showLoading(true);

  try {
    const response = await fetch("/history");
    const data = await response.json();

    if (response.ok) {
      const chatMessages = document.getElementById("chatMessages");
      chatMessages.innerHTML = "";

      if (data.conversations.length === 0) {
        addMessage("bot", "履歴がありません。新しい会話を始めましょう！");
      } else {
        data.conversations.reverse().forEach((conv) => {
          addMessage("user", conv.user_message);
          addMessage("bot", conv.bot_response, {
            sentiment: conv.sentiment,
            intent: conv.intent,
          });
        });
      }
    } else {
      addMessage("bot", "履歴の読み込みに失敗しました。");
    }
  } catch (error) {
    console.error("Error loading history:", error);
    addMessage("bot", "履歴の読み込み中にエラーが発生しました。");
  }

  showLoading(false);
}

async function showAnalytics() {
  showLoading(true);

  try {
    const response = await fetch("/analytics");
    const data = await response.json();

    if (response.ok) {
      displayAnalytics(data);
    } else {
      alert("分析データの取得に失敗しました。");
    }
  } catch (error) {
    console.error("Error loading analytics:", error);
    alert("分析データの取得中にエラーが発生しました。");
  }

  showLoading(false);
}

function displayAnalytics(data) {
  const modal = document.getElementById("analyticsModal");
  const sentimentChart = document.getElementById("sentimentChart");
  const intentChart = document.getElementById("intentChart");

  // 感情分析チャート
  sentimentChart.innerHTML = "";
  if (data.sentiment_analysis.length > 0) {
    data.sentiment_analysis.forEach((item) => {
      const chartItem = document.createElement("div");
      chartItem.className = "chart-item";
      chartItem.innerHTML = `
                <span class="chart-label">${getSentimentEmoji(
                  item.sentiment
                )} ${item.sentiment}</span>
                <span class="chart-value">${item.count}回</span>
            `;
      sentimentChart.appendChild(chartItem);
    });
  } else {
    sentimentChart.innerHTML = "<p>感情分析データがありません。</p>";
  }

  // 意図分析チャート
  intentChart.innerHTML = "";
  if (data.top_intents.length > 0) {
    data.top_intents.forEach((item) => {
      const chartItem = document.createElement("div");
      chartItem.className = "chart-item";
      chartItem.innerHTML = `
                <span class="chart-label">🎯 ${getIntentLabel(
                  item.intent
                )}</span>
                <span class="chart-value">${item.count}回</span>
            `;
      intentChart.appendChild(chartItem);
    });
  } else {
    intentChart.innerHTML = "<p>意図分析データがありません。</p>";
  }

  // モーダルを表示
  modal.style.display = "block";
}

function closeAnalytics() {
  const modal = document.getElementById("analyticsModal");
  modal.style.display = "none";
}

// モーダルの外側をクリックしたら閉じる
window.onclick = function (event) {
  const modal = document.getElementById("analyticsModal");
  if (event.target === modal) {
    modal.style.display = "none";
  }
};

// エスケープキーでモーダルを閉じる
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    const modal = document.getElementById("analyticsModal");
    if (modal.style.display === "block") {
      modal.style.display = "none";
    }
  }
});
