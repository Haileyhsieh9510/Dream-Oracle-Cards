import csv
import os
from datetime import datetime

def save_result(keyword, dream_text, emotion, card):
    """
    將輸入的夢境、解析、情緒、卡牌建議寫入 CSV 檔案
    """
    output_dir = "output"
    output_file = os.path.join(output_dir, "dream_log.csv")

    # 確保 output 資料夾存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 檢查檔案是否已存在（決定是否寫入標題）
    file_exists = os.path.isfile(output_file)

    with open(output_file, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "keyword", "emotion", "title", "message", "dream_text"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            keyword,
            emotion,
            card["title"],   # ✅ 卡牌標題
            card["message"],      # ✅ 建議文字（原本錯寫為 card["message"]）
            dream_text
        ])
