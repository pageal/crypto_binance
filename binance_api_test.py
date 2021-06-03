import os
import sysconfig
import sys
from binance.client import Client
from binance_defines import *
from binance.enums import *
from datetime import *

#https://github.com/sammchardy/python-binance
#https://algotrading101.com/learn/binance-python-api-guide/


api_key = os.environ.get("BNB_API_KEY")
secret_key = os.environ.get("BNB_SECRET_KEY")
client = Client(api_key, secret_key)
print("API URL: " + str(client.API_URL))
dic = client.get_account()
for coin in dic["balances"]:
    if(float(coin["free"]) != 0 or float(coin["locked"])!=0):
        print("{}: {}".format(coin["asset"], coin["free"]))
#print(str(dic))




# request historical candle (or klines) data
# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
end_timestamp = datetime.now()
start_timestamp = end_timestamp - timedelta(days=10)
start_timestamp = start_timestamp.strftime("%Y-%m-%d")
end_timestamp = end_timestamp.strftime("%Y-%m-%d")
bars = client.get_historical_klines(symbol='BTCUSDT', interval=KLINE_INTERVAL_1DAY, start_str=start_timestamp, end_str=end_timestamp)

print("Binance API test is  COMPLETED")


