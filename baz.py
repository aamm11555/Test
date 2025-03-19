import requests
import json
import re
import time
import urllib3
from datetime import datetime, timezone, timedelta

# تعطيل تحذيرات SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_access_token():
    print("[+] جلب Access Token...")
    url = "https://web-api.onlinesoccermanager.com/api/tokenRefresh"
    headers = {
        "Host": "web-api.onlinesoccermanager.com",
        "Cookie": "CultureCode=en-GB; _ga=GA1.1.1806261794.1740859773; MachineId=73776764; _sharedID=0530b915-3a32-4129-b11e-2d1be6ce9985; _sharedID_cst=zix7LPQsHA%3D%3D; isFromGdprOptInCountry=false; isPrivacyNoticeAccepted=true; consumableRewardModalViewedTimestamp=1741050037; inventoryViewedLastTimestamp=1741050038; HasLoggedInBefore=true; forum_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkEgRWxzaGVyYmlueSIsImlkIjoiNzc4MDY4MTE3IiwiYXZhdGFyVXJsIjoiIiwibGFuZ3VhZ2Vjb2RlIjoiZW4iLCJuYmYiOjE3NDExMzQxNTMsImV4cCI6MTc0MTczODk1MywiaWF0IjoxNzQxMTM0MTUzfQ.p8Lxxvyejnhx3qf8o0S4jDSHkEDYJtSbTW8dhyFBJow",
        "Content-Length": "494",
        "Platformid": "11",
        "Sec-Ch-Ua-Platform": "Windows",
        "Accept-Language": "en-GB, en-GB",
        "Sec-Ch-Ua": "\"Not A(Brand)\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Appversion": "3.222.0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://en.onlinesoccermanager.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://en.onlinesoccermanager.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i"
    }
    data = {
        "grant_type": "refresh_token",
        "client_id": "jPs3vVbg4uYnxGoyunSiNf1nIqUJmSFnpqJSVgWrJleu6Ak7Ga",
        "client_secret": "ePOVDMfAvU8zcyfaxLMtqYSmND3n6vmmKx9ZlVnNGjGkzucMCt",
        "refresh_token": "eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJPU00uQXV0aGVudGljYXRpb24iLCJleHAiOjE3NDMwMDk5OTAsIm5iZiI6MTc0MjQwNTE5MCwiaWQiOjc3MTE1OTc4NiwidG9rZW4iOiJiZmNhYWNmYy01OGNhLTQ1YWUtODAxOS0wZmYyYjlmOTIxZjIiLCJpYXQiOjE3NDI0MDUxOTB9.dlSptS3nvA3EMDEARs1woE8g_fo1mWKhYOMZsr7Ssnk"
    }
    response = requests.post(url, headers=headers, data=data, verify=False, allow_redirects=False)
    try:
        response_json = response.json()
        if "access_token" in response_json:
            token = response_json["access_token"]
            print("[+] Access Token تم الحصول عليه بنجاح!")
            return token
    except json.JSONDecodeError:
        pass
    return None

def run_bb_ss():
    try:
        access_token = get_access_token()
        if not access_token:
            return
        print("[+] بدء استخراج الأكواد...")
        collected_ids = []
        url_bb = "https://web-api.onlinesoccermanager.com/api/v1.1/user/videos/watched"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json; charset=utf-8",
        }
        data = "actionId=Shop&rewardVariation=1&capVariation=2"
        while True:
            response = requests.post(url_bb, headers=headers, data=data)
            if "Cap reached" in response.text:
                print("[+] تم الوصول إلى الحد الأقصى، بدء تنفيذ SS...")
                break
            match = re.search(r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", response.text)
            if match:
                collected_ids.append(match.group(0))
                print(match.group(0))  # طباعة الكود فقط
                time.sleep(2)
        
        print("[+] انتهى استخراج الأكواد، جاري تنفيذ SS...")
        print("-" * 50)
        
        # استخدام الأكواد المجمعة
        url_ss = "https://web-api.onlinesoccermanager.com/api/v1/user/bosscoinwallet/consumereward"
        headers_ss = {
            "Host": "web-api.onlinesoccermanager.com",
            "Platformid": "11",
            "Sec-Ch-Ua-Platform": "Windows",
            "Authorization": f"Bearer {access_token}",
            "Accept-Language": "en-GB, en-GB",
            "Sec-Ch-Ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Appversion": "3.221.0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "Accept": "application/json; charset=utf-8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://en.onlinesoccermanager.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://en.onlinesoccermanager.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=1, i"
        }
        
        for reward_id in collected_ids:
            data = {"rewardId": reward_id}
            response = requests.post(url_ss, headers=headers_ss, data=data)
            print(f"[+] تجربة rewardId: {reward_id} -> الحالة: {response.status_code}")
            print(response.text)
            print("-" * 50)
            
    except KeyboardInterrupt:
        print("[-] تم إيقاف السكربت من قبل المستخدم.")

if __name__ == "__main__":
    run_bb_ss()
