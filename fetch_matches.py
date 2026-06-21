import os
import requests
import json
from datetime import datetime

def fetch_and_save_data():
    api_key = os.environ.get('FOOTBALL_API_TOKEN')
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        all_matches = data.get('matches', [])

        # ترتيب المباريات: المباشر أولاً، ثم القادم، ثم المنتهي
        # هذا يضمن أنك دائماً تشوف الأهم
        def sort_key(m):
            status = m['status']
            if status == 'IN_PLAY': return 0
            if status == 'TIMED': return 1
            if status == 'FINISHED': return 2
            return 3

        sorted_matches = sorted(all_matches, key=sort_key)

        # تجهيز البيانات ببيانات نظيفة (بدون null)
        clean_matches = []
        for match in sorted_matches[:10]: # نأخذ أول 10 مباريات فقط
            home_score = match['score']['fullTime']['home']
            away_score = match['score']['fullTime']['away']
            
            clean_matches.append({
                "home": match['homeTeam']['shortName'] or match['homeTeam']['name'],
                "away": match['awayTeam']['shortName'] or match['awayTeam']['name'],
                "score_home": home_score if home_score is not None else "-",
                "score_away": away_score if away_score is not None else "-",
                "status": match['status']
            })

        with open("matches.json", "w", encoding="utf-8") as f:
            json.dump({"matches": clean_matches}, f, ensure_ascii=False, indent=4)
        
        print("✅ تم التنظيف والتحديث بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
