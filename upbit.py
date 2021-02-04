import requests
import pyupbit
from time import sleep

WAITTIME=0.1

def sleepTime(func):
    def in_func(*args, **kwargs):
        sleep(Upbit.WAITTIME)
        result = func(*args, **kwargs)
        return result

    return in_func

class Upbit():

    stocks_list = []

    def __init__(self):
        print()

    def start(self):
        Upbit.stocks_list = self.getStocksList()



    def getStocksList(self):
        t_stocks_list = pyupbit.get_tickers(fiat="KRW")
        return t_stocks_list

    @sleepTime
    def getStocks_info(self, stockCode):
        '''

        :param stockCode: input stocks tickers. ex) KRW-BTC
        :return:
        '''


if __name__ == '__main__':
    print('PyCharm')
