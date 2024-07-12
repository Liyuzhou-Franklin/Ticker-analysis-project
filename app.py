from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods = ['POST'])
def result():
    ticker = request.form['ticker']
    stock_info = get_stock_info(ticker)
    return render_template('result.html', stock_info=stock_info)

def get_stock_info(ticker):
    url = f"https://seeking-alpha.p.rapidapi.com/symbols/get-chart"
    querystring = {"symbol": ticker}
    headers = {
        "x-rapidapi-key": "6e90a4cc5amsh9324a55e6e118a5p1f97c2jsn28aa5a6e6a0a",
        "x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)
    date = "2024-07-11 00:00:00"
    stock_data = data['attributes'][date]

    title = ticker
    price = stock_data
    bullbearcase = "Will soon implement"

    return {
        "title": title,
        "price": price,
        "description": bullbearcase
    }

if __name__ == '__main__':
    app.run(debug=True)
