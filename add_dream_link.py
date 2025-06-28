# add_dream_link.py
import json
import os

def load_links(path="dream_links.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_links(data, path="dream_links.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    links = load_links()

    while True:
        keyword = input("🔍 請輸入夢境關鍵字（輸入 q 離開）：").strip()
        if keyword.lower() == "q":
            break

        url = input("🔗 請輸入對應網址：").strip()
        if not url.startswith("http"):
            print("⚠️ 網址格式錯誤，請重新輸入")
            continue

        links[keyword] = url
        print(f"✅ 已新增：{keyword} -> {url}")

    save_links(links)
    print("💾 已儲存到 dream_links.json")

if __name__ == "__main__":
    main()
