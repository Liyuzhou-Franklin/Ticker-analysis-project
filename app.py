from flask import Flask, request, render_template
import requests

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
    url = f"https://seeking-alpha.p.rapidapi.com/auto-complete"
    querystring = {"term": ticker}

    headers = {
        "x-rapidapi-key": "6e90a4cc5amsh9324a55e6e118a5p1f97c2jsn28aa5a6e6a0a",
        "x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

## Basically, when I tried to print out response, I didn't see the stock price.
## I tried using the get-realtime-prices endpoint, but it doesn't return anything.

    title = ticker
    price = "Stuck on getting the price"
    bullbearcase = "Stuck here as well"

    return {
        "title": title,
        "price": price,
        "description": bullbearcase
    }


"""
* This is my previous code without using the API. It fails because Seeking Alpha blocks bot requests.

from flask import Flask, request, render_template
import requests
import time
from bs4 import BeautifulSoup

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
    url = f"https://seekingalpha.com/symbol/{ticker}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    while response.status_code != 200:
        time.sleep(5)
        response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1',
        attrs={
            'class': 'ehZAr m-0 block pr-16 text-8x-large-b lg:inline-block lg:pr-0 lg:text-4x-large-b'
        }
                      ).text.strip()
    price = soup.find('span',
        attrs={
            'class': 'text-6x-large-b md:leading-none',
            'data-test-id': 'symbol-price'
        }
                      ).text.strip()
    description = soup.find('div',
        attrs={
            'class': 'viziA text-small-r text-share-text-3 lg:text-small-r',
            'data-test-id': 'symbol-description'
        }
                            ).text.strip()

    return {
        "title": title,
        "price": price,
        "description": description
    }

if __name__ == '__main__':
    app.run(debug=True)
"""