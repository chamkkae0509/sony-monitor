import requests
import time
import requests
import time
import os


URL = "https://store.sony.co.kr/product-view/131844793"

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
    res = requests.get(URL)
    html = res.text

    if "/order/sheet" in html:
        print("🔥 구매 가능!", flush=True)
        send_telegram("🔥 소니 재입고!\n지금 바로 구매하세요:\n" + URL)
        break
    else:
        print("아직 품절 상태", flush=True)

    time.sleep(5)
