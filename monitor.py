import requests
import time
import os

API_URL = "https://shop-api.e-ncp.com/products/132237901/options"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)

print("모니터링 시작", flush=True)

while True:
    try:
        res = requests.get(API_URL)
        data = res.json()

        if "flatOptions" in data and len(data["flatOptions"]) > 0:
            sale_type = data["flatOptions"][0]["saleType"]
            print("현재 상태:", sale_type, flush=True)

            if sale_type == "AVAILABLE":
                print("🔥 구매 가능!", flush=True)
                send_telegram("🔥 재입고 발생!")
                break
        else:
            print("옵션 정보 없음", flush=True)

    except Exception as e:
        print("에러 발생:", e, flush=True)

    time.sleep(3)
