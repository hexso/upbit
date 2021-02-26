import requests
import pyupbit
from datetime import date
from time import sleep
from functools import wraps
import json

WAITTIME=0.01
LOGFILE='upbit_trade.txt'
def SleepTime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sleep(WAITTIME)
        result = func(*args, **kwargs)
        return result

    return wrapper

def WithLog(func):
    import logging
    import logging.handlers

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    fileHandler = logging.FileHandler(LOGFILE)
    streamHander = logging.StreamHandler()
    fileHandler.setFormatter(formatter)
    streamHander.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHander)

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(''.format(args,kwargs))
        result = func(*args, **kwargs)
        return result

    return wrapper

class UpbitTrade:

    stocks_list = []
    selected_coin = ''
    upbit = None
    def __init__(self):
        print("Upbit is initiate.")

    def Login(self, access_key, secret_key):
        UpbitTrade.upbit = pyupbit.Upbit(access_key, secret_key)
        print(UpbitTrade.upbit.get_balances())
        #error handle required

    @WithLog
    @SleepTime
    def GetBalance(self, coin=None):
        '''

        :return:
        '''
        if  UpbitTrade.upbit == None:
            print("please login first")
            return -1
        balance = UpbitTrade.upbit.get_balances(coin)
        print(balance)
        return balance

    @WithLog
    @SleepTime
    def SendBuying(self, stockcode, amount, trade, price=None):
        '''

        :param stockcode:
        :param amount:
        :param type: 0은 지정가, 1은 시장가
        :param price: 지정가일 경우 필요.
        :return: uuid, ord_type, price, state,volume, remaining_volume etc..
        '''
        Trade = {'지정가' : 0, '시장가' : 1}
        try :
            tradeType = Trade[trade]
        except KeyError as e:
            print('Wrong trade type')
            return 0

        if tradeType == 0:
            result = UpbitTrade.upbit.buy_limit_order(stockcode, price, amount)
        elif tradeType == 1:
            result = UpbitTrade.upbit.buy_market_order(stockcode,amount)

        return result

    @WithLog
    @SleepTime
    def SendSelling(self, stockcode, amount, trade, price=None):
        Trade = {'지정가': 0, '시장가': 1}
        try:
            tradeType = Trade[trade]
        except KeyError as e:
            print('Wrong trade type')
            return 0

        if tradeType == 0:
            result = UpbitTrade.upbit.sell_limit_order(stockcode, price, amount)
        elif tradeType == 1:
            result = UpbitTrade.upbit.sell_market_order(stockcode, amount)

        return result

    @WithLog
    @SleepTime
    def CancelOrder(self, uuid):
        return UpbitTrade.upbit.cancel_order(uuid)

    @SleepTime
    def GetStocksList(self, money="KRW"):
        t_stocks_list = pyupbit.get_tickers(fiat=money)
        return t_stocks_list

    @SleepTime
    def GetDayCandle(self, stockcode, count=1):
        '''
        :param stockcode: input stocks tickers. ex) KRW-BTC
        :return: dictionary is in list.
                opening_price, high_price, low_price, trade_price,
                candle_acc_trade_price, candle_acc_trade_volume,
                change_price, change_rate
        '''
        url = "https://api.upbit.com/v1/candles/days"
        querystring = {"market": stockcode, "count": count}
        response = requests.request("GET", url, params=querystring)
        json_data = json.loads(response.text)
        return json_data

    @SleepTime
    def GetMinCandle(self, stockcode, mins='1', count=1):
        '''

        :param stockcode: input stocks tickers. ex) KRW-BTC
        :return: dictionary is in list.
                opening_price, high_price, low_price, trade_price,
                candle_acc_trade_price, candle_acc_trade_volume,
                change_price, change_rate
        '''
        if type(mins) == type(1) :
            mins = str(mins)
        url = "https://api.upbit.com/v1/candles/minutes/" + mins
        querystring = {"market": stockcode, "count": count}
        response = requests.request("GET", url, params=querystring)
        json_data = json.loads(response.text)
        return json_data

    @SleepTime
    def GetCurrentPrice(self, stockcode):
        return pyupbit.get_current_price(stockcode)

if __name__ == '__main__':
    print('PyCharm')
