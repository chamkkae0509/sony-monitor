import os, time, requests

API_URL = "https://shop-api.e-ncp.com/products/132237901/options"

HEADERS = {
    "Version": os.getenv("SHOPBY_VERSION", "1.0"),
    "clientId": os.getenv("SHOPBY_CLIENT_ID", ""),   # 반드시 채워야 할 가능성 큼
    "platform": os.getenv("SHOPBY_PLATFORM", "PC"),  # PC / MOBILE_WEB / AOS / IOS 중 하나
    "Accept": "application/json",
    "User-Agent": "stock-monitor/1.0",
}

def fetch_json():
    res = requests.get(API_URL, headers=HEADERS, timeout=10)
    if res.status_code != 200:
        # 400일 때 원인 메시지가 여기 들어오는 경우가 많음
        print("HTTP", res.status_code, "body:", res.text[:500], flush=True)
        res.raise_for_status()
    return res.json()

while True:
    try:
        data = fetch_json()
        opt = (data.get("flatOptions") or [{}])[0]
        print("saleType=", opt.get("saleType"), "stockCnt=", opt.get("stockCnt"), flush=True)
    except Exception as e:
        print("에러:", repr(e), flush=True)

    time.sleep(3)
