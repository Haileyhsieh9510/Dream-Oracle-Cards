# dream_parser.py
import json
import os
from bs4 import BeautifulSoup
import requests

# 載入自訂關鍵字網址對應表
def load_dream_links():
    path = "dream_links.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

dream_links = load_dream_links()

# ✅ 直接從網址爬取夢境內容
def crawl_dream_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = "utf-8"

        if resp.status_code != 200:
            return "⚠️ 無法載入夢境解析頁面"

        soup = BeautifulSoup(resp.text, "html.parser")
        body_div = soup.find("div", id="entrybody")
        if not body_div:
            return "⚠️ 找不到夢境解析內容"

        return body_div.get_text(separator="\n", strip=True)

    except Exception as e:
        return f"⚠️ 發生錯誤：{e}"

# ✅ 解夢主邏輯
def get_dream_interpretation(keyword):
    if keyword in dream_links:
        url = dream_links[keyword]
        return crawl_dream_from_url(url)

    return "⚠️ 尚未支援此夢境，請稍後再試或由開發者補充資料"
