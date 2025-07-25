import requests
import json
import time

API_URL = "https://www.ekiten.jp/api/shop-search/area/cities/"
CITY_URL_TEMPLATE = "https://www.ekiten.jp/area/a_pref{pre_code}/a_city{city_code}/"
OUTPUT_FILE = "../ekiten_cities.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EkitenScraper/2.0)"
}

# 都道府県名と2桁コード（01〜47）
pref_codes = [
    ("北海道", "01"), ("青森県", "02"), ("岩手県", "03"), ("宮城県", "04"), ("秋田県", "05"), ("山形県", "06"), ("福島県", "07"),
    ("茨城県", "08"), ("栃木県", "09"), ("群馬県", "10"), ("埼玉県", "11"), ("千葉県", "12"), ("東京都", "13"), ("神奈川県", "14"),
    ("新潟県", "15"), ("富山県", "16"), ("石川県", "17"), ("福井県", "18"), ("山梨県", "19"), ("長野県", "20"),
    ("岐阜県", "21"), ("静岡県", "22"), ("愛知県", "23"), ("三重県", "24"), ("滋賀県", "25"), ("京都府", "26"), ("大阪府", "27"),
    ("兵庫県", "28"), ("奈良県", "29"), ("和歌山県", "30"), ("鳥取県", "31"), ("島根県", "32"), ("岡山県", "33"), ("広島県", "34"),
    ("山口県", "35"), ("徳島県", "36"), ("香川県", "37"), ("愛媛県", "38"), ("高知県", "39"), ("福岡県", "40"), ("佐賀県", "41"),
    ("長崎県", "42"), ("熊本県", "43"), ("大分県", "44"), ("宮崎県", "45"), ("鹿児島県", "46"), ("沖縄県", "47")
]

def get_city_list(pref_code):
    data = {
        "searchConditions": {
            "searchServiceType": "inShop",
            "prefectureCode": pref_code,
            "cityCode": "",
            "trainRouteId": "",
            "stationIds": [],
            "busStopIds": [],
            "townAreaIds": [],
            "largeGenreCode": "",
            "smallGenreCode": "",
            "featureIds": [],
            "shopMenuKindIds": [],
            "distance": ""
        },
        "needsIndex": True,
        "isFromFreeWordPage": False
    }
    params = {"data": json.dumps(data, ensure_ascii=False)}
    resp = requests.get(API_URL, params=params, headers=HEADERS)
    resp.raise_for_status()
    result = resp.json()
    city_list = []
    for kana_group in result.get("data", []):
        for city in kana_group.get("contents", []):
            city_code = city.get("code")
            city_name = city.get("name")
            if city_code and city_name:
                city_url = CITY_URL_TEMPLATE.format(pre_code=pref_code, city_code=city_code)
                city_list.append({"name": city_name, "url": city_url, "code": city_code})
    return city_list

def main():
    all_data = []
    for pref_name, pref_code in pref_codes:
        try:
            print(f"Scraping {pref_name} ({pref_code}) ...")
            cities = get_city_list(pref_code)
            all_data.append({
                "prefecture": pref_name,
                "cities": cities
            })
            time.sleep(1)  # サイト負荷軽減
        except Exception as e:
            print(f"Error scraping {pref_name}: {e}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
