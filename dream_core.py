# dream_core.py
import random
import os
from datetime import datetime
from dream_parser import get_dream_interpretation
from emotion_mapper import map_emotion
from oracle_engine import draw_card
from utils import save_result

# ✅ 新增：LINE Push API 相關套件
from linebot.v3 import Configuration
from linebot.v3.messaging import MessagingApi, ApiClient, TextMessage

# 備用卡牌圖片清單（請依實際圖片命名調整）
ALL_CARD_IMAGES = [
    "A1.jpg", "A2.jpg", "A3.jpg", "B1.jpg", "B2.jpg", "B3.jpg", "C1.jpg", "C2.jpg", "c3.jpg", "D1.jpg", "D2.jpg", "D3.jpg",
    "E1.jpg", "E2.jpg", "E3.jpg", "F1.jpg", "F2.jpg", "F3.jpg", "G1.jpg", "G2.jpg", "G3.jpg", "H1.jpg", "H2.jpg", "H3.jpg",
    "I1.jpg", "I2.jpg", "I3.jpg", "J1.jpg", "J2.jpg", "J3.jpg", "K1.jpg", "K2.jpg", "K3.jpg", "L1.jpg", "L2.jpg", "L3.jpg",
    "M1.jpg", "M2.jpg", "M3.jpg", "N1.jpg", "N2.jpg", "N3.jpg", "O1.jpg", "O2.jpg", "O3.jpg", "P1.jpg", "P2.jpg", "P3.jpg"
]

def process_dream(keyword, user_id=None):
    dream_text = get_dream_interpretation(keyword)

    if dream_text.startswith("⚠️"):
        # ✅ 寫入 missing log
        log_dir = "output"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        with open(os.path.join(log_dir, "missing_keywords.log"), "a", encoding="utf-8") as f:
            line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {user_id or 'anonymous'} | {keyword}\n"
            f.write(line)

        # ✅ 發 LINE 推播通知開發者（你）
        developer_user_id = os.getenv("DEVELOPER_USER_ID")
        if developer_user_id:
            message = f"🛑 使用者 {user_id or 'unknown'} 查詢「{keyword}」，但查無解夢資料"
            configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.push_message(
                    to=developer_user_id,
                    messages=[TextMessage(text=message)]
                )

        # ✅ 回傳預設卡牌
        emotion = "未知"
        card = {
            "title": "無法對應情緒",
            "message": "👉 目前僅支援特定情緒，將為你抽一張隨機命定卡。",
            "image": random.choice(ALL_CARD_IMAGES)
        }
    else:
        emotion = map_emotion(dream_text)
        card = draw_card(emotion)

    save_result(keyword, dream_text, emotion, card)

    text = f"""🔍 解夢關鍵字：{keyword}
🧠 解夢結果：
{dream_text}

🎭 情緒判定：{emotion}
🃏 命定卡牌：「{card['title']}」
👉 {card['message']}"""

    return {
        "text": text,
        "image": card["image"]
    }
