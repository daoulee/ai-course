import json
import os

import requests
from flask import Flask, render_template, request

SECRET_KEY = os.environ.get("TOSS_SECRET_KEY", "test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6")
CONFIRM_URL = "https://api.tosspayments.com/v1/payments/confirm"
PRICE = 1000

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/success")
def success():
    payment_key = request.args.get("paymentKey", "")
    order_id = request.args.get("orderId", "")
    amount = request.args.get("amount", "")

    if amount != str(PRICE):
        return render_template("success.html", ok=False, status_code="-",
                               code="AMOUNT_MISMATCH",
                               message=f"요청 금액 {amount}원이 상품 금액 {PRICE}원과 다릅니다. 승인하지 않았습니다.")

    r = requests.post(CONFIRM_URL, auth=(SECRET_KEY, ""),
                      json={"paymentKey": payment_key, "orderId": order_id, "amount": PRICE})
    data = r.json()
    raw = json.dumps(data, ensure_ascii=False, indent=2)

    if r.status_code != 200:
        return render_template("success.html", ok=False, status_code=r.status_code,
                               code=data.get("code"), message=data.get("message"), raw=raw)
    return render_template("success.html", ok=True, data=data, raw=raw)


@app.get("/fail")
def fail():
    return render_template("fail.html", code=request.args.get("code", ""),
                           message=request.args.get("message", ""))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
