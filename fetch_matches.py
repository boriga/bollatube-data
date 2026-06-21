import os
import requests
import json

def fetch_all_tournament_data():
    api_key = os.environ.get('FOOTBALL_API_TOKEN')
    base_url = "https://api.football-data.org/v4/competitions/WC"
    headers = {"X-Auth-Token": api_key}

    # قائمة المسارات التي نريد جلبها
    endpoints = {
        "matches": f"{base_url}/matches",
        "standings": f"{base_url}/standings",
        "scorers": f"{base_url}/scorers"
    }

    for name, url in endpoints.items():
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # حفظ كل نوع في ملف خاص
                with open(f"{name}.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"✅ تم تحديث {name}.json بنجاح")
            else:
                print(f"❌ خطأ في جلب {name}: {response.status_code}")
        except Exception as e:
            print(f"❌ حدث خطأ تقني في {name}: {e}")

if __name__ == "__main__":
    fetch_all_tournament_data()
