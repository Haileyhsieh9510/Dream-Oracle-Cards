
import pandas as pd
import random

# 讀取 CSV 資料檔（請確認路徑與檔案存在）
CSV_PATH = "emotion_cards_full.csv"
df = pd.read_csv(CSV_PATH)

def draw_card(emotion: str) -> dict:
    """
    根據輸入情緒選擇一張命定卡牌，若無符合則回傳預設卡。
    """
    # 定義同義情緒對應（可自行擴充）
    synonym_map = {
        "愛": "被愛",
        "幸福感": "幸福",
    }
    mapped_emotion = synonym_map.get(emotion, emotion)

    # 篩選符合情緒的卡牌
    matched = df[df["emotion"] == mapped_emotion]

    if matched.empty:
        return {
            "title": "（替代推薦）每次感到迷惘，都是更認識自己的機會。",
            "message": "試著寫日記，記錄最近的想法與感受。",
            "image": "J2.jpg"
        }   

    selected = matched.sample(n=1).iloc[0]
    return {
    "title": selected["title"],
    "message": selected["message"],
    "image": selected["image"]
    }

# 範例測試（可移除）
if __name__ == "__main__":
    test_emotion = "愛"
    card = draw_card(test_emotion)
    print(f"🎭 情緒判定：{test_emotion}")
    print(f"🃏 命定卡牌：「{card['title']}」")
    print(f"👉 {card['message']}")
    print(f"🖼️ 對應圖片檔名： {card['image']}")
