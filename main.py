import upbit
import average_candle
import sys

class AutoBot():
    trader = None

    def __init__(self, trader):
        AutoBot.trader = trader
        f = open('private.txt','r')
        accessKey = f.readline()
        privateKey =f.readline()
        print('{} privatekey is {}'.format(accessKey,privateKey))
        AutoBot.trader.login(accessKey, privateKey)

    def start(self, algorithm):
        algorithm.start()

    def getBalance(self):
        return AutoBot.trader.getBalance()

    def sendBuying(self, stockCode, amount, trade, price=None):
        return AutoBot.trader.sendBuying(stockCode, amount, trade, price)

    def sendSelling(self, stockCode, amount, trade, price=None):
        return AutoBot.trader.sendSelling(stockCode, amount, trade, price)

    def getStocksList(self, money='KRW'):
        return AutoBot.trader.getStocksList(money)

    def getDayCandle(self, stockCode):
        return AutoBot.trader.getDayCandle(stockCode)

    def getMinCandle(self, stockCode):
        return AutoBot.trader.getMinCandle(stockCode)

    def getCurrentPrice(self, stockCode):
        return AutoBot.trader.getCurrentPrice(stockCode)

    def CancelOrder(self, uuid):
        return AutoBot.trader.CancelOrder(uuid)

    def help(self):
        print('자동 매매는 1, 차트 분석 및 알림은 2')


if __name__ == '__main__':
    '''
    Upbit
    '''
    help()
    trader = upbit.UpbitTrade()
    autoTrader = AutoBot(trader)
    algorithm = average_candle.AvgCandle(autoTrader)
    autoTrader.start(algorithm)

