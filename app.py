from flask import Flask, request, render_template
from datetime import datetime, timedelta
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

def get_last_workday():
    today = datetime.today()
    if today.weekday() == 0:
        last_workday = today - timedelta(days=3)
    elif today.weekday() == 6:
        last_workday = today - timedelta(days=2)
    else:
        last_workday = today - timedelta(days=1)

    last_workday_str = last_workday.strftime('%Y-%m-%d 00:00:00')
    return last_workday_str

def get_stock_info(ticker):
    url = f"https://seeking-alpha.p.rapidapi.com/symbols/get-chart"
    querystring = {"symbol": ticker}
    headers = {
        "x-rapidapi-key": "6e90a4cc5amsh9324a55e6e118a5p1f97c2jsn28aa5a6e6a0a",
        "x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    date = get_last_workday()
    stock_data = data['attributes'][date]

    url2 = f"https://seeking-alpha.p.rapidapi.com/analysis/list"
    querystring = {"id": ticker}
    response2 = requests.request("GET", url2, headers=headers, params=querystring)
    data2 = response2.json()
    article_links = [article['links']['self'] for article in data2['data']]
    articles_list = []
    for link in article_links:
        articles_list.append("seekingalpha.com" + link)

    return {
        "title": ticker,
        "price": stock_data,
        "articles": articles_list
    }

if __name__ == '__main__':
    app.run(debug=True)
