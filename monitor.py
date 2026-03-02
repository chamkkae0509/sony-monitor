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

from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

button = soup.find("a", class_="btn_style direct")

if button:
    print("🔥 구매 가능!")
else:
    print("아직 품절 상태")
    
    time.sleep(5)
