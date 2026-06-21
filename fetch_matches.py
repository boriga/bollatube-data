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

        # منطق التصفية الذكي:
        all_matches = data.get('matches', [])
        
        # 1. نبحث عن المباريات المباشرة (IN_PLAY)
        live = [m for m in all_matches if m['status'] == 'IN_PLAY']
        
        # 2. نبحث عن المباريات القادمة (TIMED)
        upcoming = [m for m in all_matches if m['status'] == 'TIMED']
        
        # 3. إذا لم يوجد مباشر أو قادم، نأخذ آخر المباريات التي انتهت (FINISHED)
        finished = [m for m in all_matches if m['status'] == 'FINISHED']
        
        # ندمج القوائم: (المباشر + القادم + آخر 3 منتهية)
        filtered_matches = live + upcoming + finished[-3:]
        
        # نأخذ أول 8 من المزيج الجديد
        final_data = {"matches": filtered_matches[:8]}

        with open("matches.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        
        print("✅ تم تحديث التصفية بنجاح!")
        
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
