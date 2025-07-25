from supabase import create_client, Client
import json

# 必要に応じてpip install supabase
# Project URLとAPIキーを設定
url = "https://opfkufedgvrnmjvnsstw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wZmt1ZmVkZ3Zybm1qdm5zc3R3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMxODg3MzAsImV4cCI6MjA2ODc2NDczMH0.I1nicCIAB7cvKZuXu-qwbThoI8g9OyXvTCiW1MGnlkU"
supabase: Client = create_client(url, key)

with open("../ekiten_cities.json", encoding="utf-8") as f:
    data = json.load(f)

for pref in data:
    prefecture = pref["prefecture"]
    for city in pref["cities"]:
        supabase.table("cities").insert({
            "prefecture": prefecture,
            "city": city["name"],
            "url": city["url"],
            "city_code": city["code"]
        }).execute()

print("データ投入完了")
