import requests
import time

URL = "https://store.sony.co.kr/product-view/132237901"

BOT_TOKEN = "8635320559:AAE7xUfiWhSrigDhvPgkZOQ8SknrlyQqkPo"
CHAT_ID = "8590643905"

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
        print("🔥 구매 가능 상태!", flush=True)
        send_telegram("🔥 소니 제품 구매 가능!\n바로 접속하세요:\n" + URL)
        break
    else:
        print("아직 품절 상태", flush=True)

    time.sleep(5)

send_telegram("✅ 테스트 메시지")
