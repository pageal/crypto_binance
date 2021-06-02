import os
import sysconfig
import sys
from binance.client import Client

#https://github.com/sammchardy/python-binance

api_key = os.environ.get("BNB_API_KEY")
secret_key = os.environ.get("BNB_SECRET_KEY")
client = Client(api_key, secret_key)
print("API URL: " + str(client.API_URL))
dic = client.get_account()
for coin in dic["balances"]:
    if(float(coin["free"]) != 0 or float(coin["locked"])!=0):
        print("{}: {}".format(coin["asset"], coin["free"]))
print(str(dic))

