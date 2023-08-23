import requests
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
ACCOUNT_SID = "AC5462615691ef27e8964844aa6956e647"
AUTH_TOKEN = os.environ.get("NEWS_AUTH_TOKEN")


# Stock
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
stock_response = requests.get(url=STOCK_API_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()
yesterday_stock_price = float(stock_data["Time Series (Daily)"]["2023-08-22"]["4. close"])
day_before_yesterday_stock_price = float(stock_data["Time Series (Daily)"]["2023-08-21"]["4. close"])
percentage_change = (
        (yesterday_stock_price - day_before_yesterday_stock_price) / yesterday_stock_price * 100)
total_percentage_change = percentage_change.__round__()

symbol = None
if yesterday_stock_price > day_before_yesterday_stock_price:
    symbol = "🔺"
else:
    symbol = "🔻"

# News
news_parameters = {
    "q": COMPANY_NAME,
    "apikey": NEWS_API_KEY
}

news_response = requests.get(url=NEWS_API_ENDPOINT, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()


if abs(percentage_change) > 5:
    for lp in range(0,3):
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            body=f"{STOCK} {symbol} {total_percentage_change}% \n Headline: {news_data['articles'][lp]['title']}\n Brief : {news_data['articles'][lp]['description']}",
            from_='+17622207574',
            to='+917397262921'
        )
        print(message.status)

