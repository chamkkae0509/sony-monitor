import os, time, random, requests

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
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)

print("모니터링 시작", flush=True)
last_sale_type = None

while True:
    try:
        res = requests.get(API_URL, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            print("HTTP", res.status_code, "body:", res.text[:300], flush=True)
        res.raise_for_status()

        data = res.json()
        opt = (data.get("flatOptions") or [{}])[0]
        sale_type = opt.get("saleType")
        stock_cnt = opt.get("stockCnt")

        print(f"상태={sale_type}, stockCnt={stock_cnt}", flush=True)

        if last_sale_type is not None and sale_type != last_sale_type:
            if sale_type == "AVAILABLE":
                send_telegram(f"🔥 재입고! 구매 가능 상태로 변경됐어요!\n현재 상태: {sale_type}")
            else:
                send_telegram(f"📦 상태 변경: {last_sale_type} → {sale_type}")

        last_sale_type = sale_type

    except Exception as e:
        print("에러:", repr(e), flush=True)

    time.sleep(5 + random.uniform(0, 1))
