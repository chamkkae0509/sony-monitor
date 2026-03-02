import requests, time, os

API_URL = "https://shop-api.e-ncp.com/products/132237901/options"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)

last_sale_type = None
print("모니터링 시작", flush=True)

while True:
    try:
        res = requests.get(API_URL, timeout=10)
        res.raise_for_status()
        data = res.json()

        opt = (data.get("flatOptions") or [{}])[0]
        sale_type = opt.get("saleType")
        stock_cnt = opt.get("stockCnt")
        forced = opt.get("forcedSoldOut")

        print(f"상태={sale_type}, stockCnt={stock_cnt}, forcedSoldOut={forced}", flush=True)

        if sale_type is not None and last_sale_type is not None and sale_type != last_sale_type:
            send_telegram(f"상태 변경: {last_sale_type} → {sale_type} (stockCnt={stock_cnt})")
        last_sale_type = sale_type

    except Exception as e:
        print("에러:", e, flush=True)

    time.sleep(3)
