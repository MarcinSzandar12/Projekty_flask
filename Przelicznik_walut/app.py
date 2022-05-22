from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_rates():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    return data[0]["rates"]

def find_bid_by_code(code):
    rates = get_rates()
    for rate in rates:
        if rate["code"] == code:
            return rate["bid"]

@app.route('/converter', methods=['GET', 'POST'])
def convert():
    if request.method == 'GET':
        rates = get_rates()
        return render_template("form.html", rates=rates)
    elif request.method == 'POST':
        currency = request.form["currency"]
        bid = find_bid_by_code(currency)
        quantity = request.form["quantity"]
        quantity = int(quantity)
        price = quantity * bid
        return render_template("result.html", price=price)
