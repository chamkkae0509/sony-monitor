import os
import time
import random
import requests

API_URL = "https://shop-api.e-ncp.com/products/132237901/options"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SHOPBY_CLIENT_ID = os.getenv("SHOPBY_CLIENT_ID")

HEADERS = {
    "Version": "1.0",
    "clientId": SHOPBY_CLIENT_ID,
    "platform": "PC",
    "Accept": "application/json",
    "User-Agent": "stock-monitor/1.0",
}

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    res.raise_for_status()

def fetch_sale_type():
    res = requests.get(API_URL, headers=HEADERS, timeout=10)
    if res.status_code != 200:
        print("HTTP", res.status_code, "body:", res.text[:300], flush=True)
    res.raise_for_status()
    data = res.json()
    opt = (data.get("flatOptions") or [{}])[0]
    return opt.get("saleType"), opt.get("stockCnt")

# 시작 전 환경변수 체크
if not BOT_TOKEN or not CHAT_ID or not SHOPBY_CLIENT_ID:
    raise RuntimeError("BOT_TOKEN / CHAT_ID / SHOPBY_CLIENT_ID 환경변수를 확인하세요.")

print("모니터링 시작", flush=True)

last_sale_type = None

while True:
    try:
        sale_type, stock_cnt = fetch_sale_type()
        print(f"상태={sale_type}, stockCnt={stock_cnt}", flush=True)

        if last_sale_type is None:
            # 최초 실행 시 이미 구매 가능이면 즉시 알림
            last_sale_type = sale_type
            if sale_type == "AVAILABLE":
                send_telegram("이미 구매 가능 상태예요!")
        elif sale_type != last_sale_type:
            # 상태가 바뀔 때마다 알림
            if sale_type == "AVAILABLE":
                send_telegram(f"🔥 재입고! 구매 가능 상태로 변경됐어요!\n이전: {last_sale_type} → 현재: {sale_type}")
            else:
                send_telegram(f"📦 상태 변경\n이전: {last_sale_type} → 현재: {sale_type} (stockCnt={stock_cnt})")
            last_sale_type = sale_type

    except Exception as e:
        print("에러:", repr(e), flush=True)

    time.sleep(3 + random.uniform(0, 1))
