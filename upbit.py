import requests
import pyupbit
from datetime import date
from time import sleep
from functools import wraps
import json

WAITTIME=0.1
LOGFILE=date.today()
def sleepTime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sleep(WAITTIME)
        result = func(*args, **kwargs)
        return result

    return wrapper

def withLog(func):
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

class UpbitTrade():

    stocks_list = []
    selected_coin = ''
    upbit = None
    def __init__(self):
        print("Upbit is initiate.")

    def login(self, accessKey, secretKey):
        UpbitTrade.upbit = pyupbit.Upbit()
        if UpbitTrade.upbit == None:
            print("login fail")
        else :
            print("login success")


    @withLog
    @sleepTime
    def getBalance(self):
        '''

        :return:
        '''
        if  UpbitTrade.upbit == None:
            print("please login first")
            return -1
        balance = UpbitTrade.upbit.get_balances()[0]
        return balance

    @sleepTime
    def getStocksList(self, money="KRW"):
        t_stocks_list = pyupbit.get_tickers(fiat=money)
        return t_stocks_list

    @sleepTime
    def getDayCandle(self, stockCode):
        '''
        :param stockCode: input stocks tickers. ex) KRW-BTC
        :return: dictionary is in list.
                opening_price, high_price, low_price, trade_price,
                candle_acc_trade_price, candle_acc_trade_volume,
                change_price, change_rate
        '''
        url = "https://api.upbit.com/v1/candles/days"
        querystring = {"market": stockCode, "count": "1"}
        response = requests.request("GET", url, params=querystring)
        json_data = json.loads(response.text)[0]
        return json_data

    @sleepTime
    def getMinCandle(self, stockCode):
        '''

        :param stockCode: input stocks tickers. ex) KRW-BTC
        :return: dictionary is in list.
                opening_price, high_price, low_price, trade_price,
                candle_acc_trade_price, candle_acc_trade_volume,
                change_price, change_rate
        '''
        url = "https://api.upbit.com/v1/candles/minutes/1"
        querystring = {"market": stockCode, "count": "1"}
        response = requests.request("GET", url, params=querystring)
        json_data = json.loads(response.text)[0]
        return json_data


if __name__ == '__main__':
    print('PyCharm')
