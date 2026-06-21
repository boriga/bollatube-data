import os
import requests
import json

def fetch_and_save_data():
    # 1. سحب المفتاح السري من الإعدادات (GitHub Secrets)
    api_key = os.environ.get('FOOTBALL_API_TOKEN')
    
    if not api_key:
        print("خطأ: لم يتم العثور على التوكن!")
        return

    # 2. الرابط الخاص بكأس العالم
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": api_key}

    # 3. إرسال الطلب
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # التأكد من نجاح الاتصال
        
        data = response.json()

        # 4. حفظ البيانات في ملف matches.json
        with open("matches.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print("✅ تم تحديث ملف matches.json بنجاح!")
        
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
  
