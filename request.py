import requests
from flask import jsonify


API_KEY = 'SOU9H7ZZSYLHKAMD'

url = f'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=BTC&market=USD&interval=5min&apikey={API_KEY}&datatype=json'

r = requests.get(url)
data = r.json()

print(data)
