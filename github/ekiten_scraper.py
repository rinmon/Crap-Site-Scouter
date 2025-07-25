import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.ekiten.jp/"
PREF_LIST_URL = BASE_URL
CITY_LIST_URL_TEMPLATE = "https://www.ekiten.jp/?search=2&page=city&pre={:02d}"

OUTPUT_FILE = "ekiten_cities.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EkitenScraper/1.0)"
}

# 都道府県コードと名称（01〜47）
pref_codes = [
    ("北海道", 1), ("青森県", 2), ("岩手県", 3), ("宮城県", 4), ("秋田県", 5), ("山形県", 6), ("福島県", 7),
    ("茨城県", 8), ("栃木県", 9), ("群馬県", 10), ("埼玉県", 11), ("千葉県", 12), ("東京都", 13), ("神奈川県", 14),
    ("新潟県", 15), ("富山県", 16), ("石川県", 17), ("福井県", 18), ("山梨県", 19), ("長野県", 20),
    ("岐阜県", 21), ("静岡県", 22), ("愛知県", 23), ("三重県", 24), ("滋賀県", 25), ("京都府", 26), ("大阪府", 27),
    ("兵庫県", 28), ("奈良県", 29), ("和歌山県", 30), ("鳥取県", 31), ("島根県", 32), ("岡山県", 33), ("広島県", 34),
    ("山口県", 35), ("徳島県", 36), ("香川県", 37), ("愛媛県", 38), ("高知県", 39), ("福岡県", 40), ("佐賀県", 41),
    ("長崎県", 42), ("熊本県", 43), ("大分県", 44), ("宮崎県", 45), ("鹿児島県", 46), ("沖縄県", 47)
]

def scrape_city_list(pref_name, pref_code):
    url = CITY_LIST_URL_TEMPLATE.format(pref_code)
    print(f"Scraping {pref_name} ({url}) ...")
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    city_list = []
    # 市区町村リンクは aタグで、URLに"a_city"が含まれるものを抽出
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "a_city" in href:
            name = a.get_text(strip=True)
            # 絶対URL化
            city_url = href if href.startswith("http") else BASE_URL.rstrip("/") + href
            city_list.append({"name": name, "url": city_url})
    return city_list

def main():
    all_data = []
    for pref_name, pref_code in pref_codes:
        try:
            cities = scrape_city_list(pref_name, pref_code)
            all_data.append({
                "prefecture": pref_name,
                "cities": cities
            })
            time.sleep(1)  # サイト負荷軽減のため1秒待機
        except Exception as e:
            print(f"Error scraping {pref_name}: {e}")
    # JSONファイルに保存
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
