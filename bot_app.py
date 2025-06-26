# bot_app.py

from flask import Flask, request, abort, send_from_directory
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest,
    TextMessage, ImageMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from dotenv import load_dotenv
import os

from dream_core import process_dream  # ✅ 解夢邏輯核心

# 載入環境變數
load_dotenv()
configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 初始化 Flask App
app = Flask(__name__)

# ✅ 公開圖片路由：讓 /Cards/<filename> 能正確顯示
@app.route("/Cards/<path:filename>")
def serve_card_image(filename):
    return send_from_directory("Cards", filename)

# ✅ 加入首頁路由，避免 404
@app.route("/", methods=["GET"])
def index():
    return "🌙 Dream Oracle LINE BOT 正在運行中！"

# LINE Webhook 接收點
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    app.logger.info("=== LINE Webhook Received ===")
    app.logger.info("Signature: " + signature)
    app.logger.info("Body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.warning("⚠️ Invalid signature.")
        abort(400)
    except Exception as e:
        app.logger.error(f"🔥 Other error: {e}")
        abort(500)

    return 'OK'

# 處理 LINE 的文字訊息事件
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_input = event.message.text.strip()

    if user_input.lower() in ["q", "quit", "exit"]:
        reply_text = "👋 感謝使用 Dream Oracle，再會～"
        messages = [TextMessage(text=reply_text)]
    else:
        result = process_dream(user_input)
        reply_text = result["text"]
        image_filename = result["image"]

        # ✅ 正確的圖片網址路徑，注意加上 /cards/
        image_url = f"https://dream-oracle.onrender.com/Cards/{image_filename}"

        messages = [
            TextMessage(text=reply_text),
            ImageMessage(
                original_content_url=image_url,
                preview_image_url=image_url
            )
        ]

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages
            )
        )

# 本地開發啟動
if __name__ == "__main__":
    app.run(port=5001)
