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

def overall_sentiment(buy, hold, sell):
    sum = buy + hold + sell
    if (buy > sell) & (hold/sum < 0.4):
        return "buy"
    elif (sell > buy) & (hold/sum < 0.4):
        return "sell"
    else:
        return "hold"

def get_stock_info(ticker):
    querystring = {"symbol": ticker}
    querystring2 = {"id": ticker}
    headers = {
        "x-rapidapi-key": "6e90a4cc5amsh9324a55e6e118a5p1f97c2jsn28aa5a6e6a0a",
        "x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
    }

    # 1. Retrieving price information
    url = f"https://seeking-alpha.p.rapidapi.com/symbols/get-chart"
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    date = get_last_workday()
    stock_data = data['attributes'][date]

    # 2. Retrieving the ten latest Seeking Alpha articles analyzing the stock
    url2 = f"https://seeking-alpha.p.rapidapi.com/analysis/list"
    response2 = requests.request("GET", url2, headers=headers, params=querystring2)
    data2 = response2.json()
    article_links = [article['links']['self'] for article in data2['data']]
    articles_list = []
    count = 1
    for count in range(0, 10):
        for link in article_links:
            articles_list.append("seekingalpha.com" + link)

    # 3. Retrieving Seeking Alpha authors' buy/hold/sell opinions and calculating overall sentiment
    url3 = f"https://seeking-alpha.p.rapidapi.com/symbols/get-ratings"
    response3 = requests.request("GET", url3, headers=headers, params=querystring)
    data3 = response3.json()
    item = data3['data'][0]
    attributes = item['attributes']
    ratings = attributes.get('ratings', {})
    sentiment = {
        'date': attributes.get('asDate'),
        'num_buy': round(ratings.get('authorsRatingBuyCount')),
        'num_hold': round(ratings.get('authorsRatingHoldCount')),
        'num_sell': round(ratings.get('authorsRatingSellCount')),
        'overall': overall_sentiment(ratings.get('authorsRatingBuyCount'),
                                               ratings.get('authorsRatingHoldCount'),
                                               ratings.get('authorsRatingSellCount'))
    }

    # 4. Retrieving the five latest earnings call transcripts
    url4 = "https://seeking-alpha.p.rapidapi.com/transcripts/list"
    response = requests.request("GET", url4, headers=headers, params=querystring2)
    data4 = response.json()
    transcript = []
    for i in range(0, 5):
        earnings = data4['data'][i]
        link = earnings.get('links').get('self')
        transcript.append("seekingalpha.com" + link)
    
    return {
        "title": ticker,
        "price": stock_data,
        "articles": articles_list,
        "sentiment": sentiment,
        "transcript": transcript
    }

if __name__ == '__main__':
    app.run(debug=True)
