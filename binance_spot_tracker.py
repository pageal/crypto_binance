

import os
from binance.client import Client
from binance_defines import *
from binance.enums import *
from datetime import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Binance_Spot_Tracker():
    # define App password first https://support.google.com/accounts/answer/185833
    def __init__(self, api_key = os.environ.get("BNB_API_KEY"), secret_key = os.environ.get("BNB_SECRET_KEY"), \
                 sender_mail = os.environ.get("BNB_SENDER_MAIL"), \
                 sender_app_passw = os.environ.get("BNB_SENDER_APP_PASSW"), \
                 recipient_mail = os.environ.get("BNB_RECIPIENT_MAIL")):


        self.api_key = api_key
        self.secret_key = secret_key
        self.client = Client(api_key, secret_key)
        print("Binance_Spot_Tracker created with API URL: " + str(self.client.API_URL))
        self.active_coins = self.get_active_coins()
        self.sender_mail = sender_mail
        self.sender_app_passw = sender_app_passw
        self.recipient_mail = recipient_mail

    def get_active_coins(self):
        dic = self.client.get_account()
        coins = []
        for coin in dic["balances"]:
            if(float(coin["free"]) != 0 or float(coin["locked"])!=0):
                print("{}: {}".format(coin["asset"], coin["free"]))
                coins.append(coin["asset"])
        return coins

    def get_historical_bars(self,coin_pair,days_back = 10):
        # request historical candle (or klines) data
        # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        end_timestamp = datetime.now()
        start_timestamp = end_timestamp - timedelta(days=days_back)
        start_timestamp = start_timestamp.strftime("%Y-%m-%d")
        end_timestamp = end_timestamp.strftime("%Y-%m-%d")
        bars = []
        try:
            bars = self.client.get_historical_klines(symbol=coin_pair, interval=KLINE_INTERVAL_1DAY, \
                                                start_str=start_timestamp, end_str=end_timestamp)
        except Exception as e:
            #print("There are no prices for " + coin_pair)
            pass
        return bars

    def get_historical_max(self, coin_pair, days_back = 10):
        bars = self.get_historical_bars(coin_pair, days_back)
        max_val = 0
        if len(bars) == 0:
            return max_val
        for bar in bars:
            coin_highest_day_price = float(bar[OHLC_enum.PRICE_HIGHEST])
            if max_val == 0:
                max_val = coin_highest_day_price
            if coin_highest_day_price > max_val:
                max_val = coin_highest_day_price
        return max_val

    def get_historical_min(self, coin_pair, days_back = 10):
        bars = self.get_historical_bars(coin_pair, days_back)
        min_val = 0
        if len(bars) == 0:
            return min_val
        for bar in bars:
            coin_lowest_day_price = float(bar[OHLC_enum.PRICE_LOWEST])
            if min_val == 0:
                min_val = coin_lowest_day_price
            if coin_lowest_day_price < min_val:
                min_val = coin_lowest_day_price
        return min_val

    def get_current_price(self, coin_pair):
        current_price = {'price':0}
        try:
            current_price = self.client.get_symbol_ticker(symbol=coin_pair)
        except Exception as e:
            pass
        return float(current_price['price'])

    def send_gmail(self, subject, plain_text):
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = self.sender_mail
        message['To'] = self.recipient_mail
        message['Subject'] = subject
        # The body and the attachments for the mail
        message.attach(MIMEText(plain_text, 'plain'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP_SSL('smtp.gmail.com', smtplib.SMTP_SSL_PORT)  # use gmail with port
        sending_failed = False
        try:
            session.ehlo()
            session.login(self.sender_mail, self.sender_app_passw)  # login with mail_id and password
            text = message.as_string()
            session.sendmail(self.sender_mail, self.recipient_mail, text)
        except Exception as e:
            sending_failed = True
        session.quit()
        if (sending_failed):
            print('Mailing failed')
        print('Mail Sent')

    def test_historical_max(self, active_coins, percent_threshold = 5):
        dic_max_historical_prices = {}
        for coin in active_coins:
            USDT_max = st.get_historical_max(coin + 'USDT')
            if (USDT_max != 0):
                dic_max_historical_prices[coin + 'USDT'] = USDT_max
            ETH_max = st.get_historical_max(coin + 'ETH')
            if (ETH_max != 0):
                dic_max_historical_prices[coin + 'ETH'] = ETH_max
            print("{}USDT max: {}, {}ETH max: {}".format(coin, USDT_max, coin, ETH_max))

        for coin_pair, historical_max_price in dic_max_historical_prices.items():
            current_price = st.get_current_price(coin_pair)
            if (current_price > historical_max_price) and abs(current_price - historical_max_price) > percent_threshold:
                msg = "{}: current: {}, MAX: {}, delta: {}, delta%: {}".format(coin_pair, current_price,
                                                                               historical_max_price, \
                                                                               current_price - historical_max_price, \
                                                                               ((current_price - historical_max_price) / historical_max_price) * 100)
                print(msg)
                st.send_gmail("SELL on UP-tick on {}".format(coin_pair), msg)

    def test_historical_min(self, active_coins, percent_threshold = 5):
        dic_min_historical_prices = {}
        for coin in active_coins:
            USDT_max = st.get_historical_min(coin + 'USDT')
            if (USDT_max != 0):
                dic_min_historical_prices[coin + 'USDT'] = USDT_max
            ETH_max = st.get_historical_min(coin + 'ETH')
            if (ETH_max != 0):
                dic_min_historical_prices[coin + 'ETH'] = ETH_max
            print("{}USDT min: {}, {}ETH min: {}".format(coin, USDT_max, coin, ETH_max))

        for coin_pair, historical_min_price in dic_min_historical_prices.items():
            current_price = st.get_current_price(coin_pair)
            if (current_price < historical_min_price) and abs(current_price - historical_min_price) > percent_threshold:
                msg = "{}: current: {}, MIN: {}, delta: {}, delta%: {}".format(coin_pair, current_price,
                                                                               historical_min_price, \
                                                                               current_price - historical_min_price, \
                                                                               ((current_price - historical_min_price) / historical_min_price) * 100)
                print(msg)
                st.send_gmail("BUY on DOWN-tick on {}".format(coin_pair), msg)


if __name__ == '__main__':
    api_key = os.environ.get("BNB_API_KEY")
    secret_key = os.environ.get("BNB_SECRET_KEY")
    sender_mail = os.environ.get("BNB_SENDER_MAIL")
    sender_app_passw = os.environ.get("BNB_SENDER_APP_PASSW") #define App password first https://support.google.com/accounts/answer/185833
    recipient_mail = os.environ.get("BNB_RECIPIENT_MAIL")
    st = Binance_Spot_Tracker(api_key = api_key, secret_key = secret_key, sender_mail = sender_mail, sender_app_passw=sender_app_passw, recipient_mail=recipient_mail)
    active_coins = st.get_active_coins()
    st.test_historical_max(active_coins, 5)
    st.test_historical_min(active_coins, 5)
    print("Binance spot tracker FINISHED")


