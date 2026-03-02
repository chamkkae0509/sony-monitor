import requests
from bs4 import BeautifulSoup
import time

URL = "https://store.sony.co.kr/product-view/132237901"

print("모니터링 시작", flush=True)

while True:
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    button = soup.select_one("a.btn_style")

    if button:
        href = button.get("href")
        text = button.text.strip()

        print(f"현재 상태: {text}", flush=True)

        if href and href != "#none":
            print("🔥 구매 가능 상태!", flush=True)
            break

    else:
        print("버튼 찾기 실패", flush=True)

    time.sleep(10)
