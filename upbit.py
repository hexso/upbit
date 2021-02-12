import requests
import pyupbit
from datetime import date
from time import sleep
from functools import wraps
import json

WAITTIME=0.01
LOGFILE='upbit_trade.txt'
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
        UpbitTrade.upbit = pyupbit.Upbit(accessKey, secretKey)
        print(UpbitTrade.upbit.get_balances())
        if UpbitTrade.upbit == None:
            print("login fail")
        else :
            print("login success")


    @withLog
    @sleepTime
    def getBalance(self, coin=None):
        '''

        :return:
        '''
        if  UpbitTrade.upbit == None:
            print("please login first")
            return -1
        balance = UpbitTrade.upbit.get_balances(coin)
        print(balance)
        return balance

    @withLog
    @sleepTime
    def sendBuying(self, stockCode, amount, trade, price=None):
        '''

        :param stockCode:
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
            result = UpbitTrade.upbit.buy_limit_order(stockCode, price, amount)
        elif tradeType == 1:
            result = UpbitTrade.upbit.buy_market_order(stockCode,amount)

        return result

    @withLog
    @sleepTime
    def sendSelling(self, stockCode, amount, trade, price=None):
        Trade = {'지정가': 0, '시장가': 1}
        try:
            tradeType = Trade[trade]
        except KeyError as e:
            print('Wrong trade type')
            return 0

        if tradeType == 0:
            result = UpbitTrade.upbit.sell_limit_order(stockCode, price, amount)
        elif tradeType == 1:
            result = UpbitTrade.upbit.sell_market_order(stockCode, amount)

        return result

    @withLog
    @sleepTime
    def CancelOrder(self, uuid):
        return UpbitTrade.upbit.cancel_order(uuid)

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

    @sleepTime
    def getCurrentPrice(self, stockCode):
        return pyupbit.get_current_price(stockCode)

if __name__ == '__main__':
    print('PyCharm')
