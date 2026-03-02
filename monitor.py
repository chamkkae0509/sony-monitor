import requests
import time

URL = "https://store.sony.co.kr/product-view/132237901"

print("모니터링 시작", flush=True)

while True:
    res = requests.get(URL)
    html = res.text

    if "/order/sheet" in html:
        print("🔥 구매 가능 상태!", flush=True)
        break
    else:
        print("아직 품절 상태", flush=True)

    time.sleep(10)
