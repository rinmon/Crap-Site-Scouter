import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.ekiten.jp"
GENRE_URL = f"{BASE_URL}/genre/"
OUTPUT_FILE = "../ekiten_genres.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EkitenGenreScraper/1.0)"
}

def get_genres():
    resp = requests.get(GENRE_URL, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    genres = []
    for main in soup.select(".main-genre-list li a"):
        main_name = main.get_text(strip=True)
        main_url = BASE_URL + main.get("href")
        main_code = main_url.rstrip('/').split('/')[-1]  # e.g., 'g_genre01'
        subgenres = []
        # サブカテゴリ取得
        sub_resp = requests.get(main_url, headers=HEADERS)
        sub_resp.raise_for_status()
        sub_soup = BeautifulSoup(sub_resp.text, "html.parser")
        for sub in sub_soup.select(".sub-genre-list li a"):
            sub_name = sub.get_text(strip=True)
            sub_url = BASE_URL + sub.get("href")
            sub_code = sub_url.rstrip('/').split('/')[-1]  # e.g., 'g_genre0101'
            subgenres.append({"name": sub_name, "url": sub_url, "code": sub_code})
        genres.append({"name": main_name, "url": main_url, "code": main_code, "subgenres": subgenres})
        time.sleep(0.5)
    return genres

def main():
    genres = get_genres()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(genres, f, ensure_ascii=False, indent=2)
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
