import sys

print("프로그램 시작", flush=True)
print("버튼 상태:", status, flush=True)

import requests
from bs4 import BeautifulSoup
import time

URL = "https://store.sony.co.kr/product-view/132237901"

def check_button():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    button = soup.select_one("a.btn_style")

    if button:
        text = button.text.strip()
        link = button.get("href")

        print("버튼 상태:", text)

        if link == "/order/sheet":
            print("🔥 구매 가능!")
            return True

    return False


while True:
    if check_button():
        print("구매 링크 생성됨!")
        break

    time.sleep(10)
