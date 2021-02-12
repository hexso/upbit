import upbit
import average_candle

class AutoBot():
    trader = None

    def __init__(self, trader):
        AutoBot.trader = trader
        f = open('private.txt','r')
        accessKey = 'F3tbzm49cxM20CEHILBz3CvpRhxhaxnxvQhCBqlx'#f.readline()
        privateKey = 'hctDvzEukrI87RnwfinQ0YsI8qAonuUUWohAn4AL'#f.readline()
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

if __name__ == '__main__':
    '''
    Upbit를 이용하여 거래
    '''
    trader = upbit.UpbitTrade()
    autoTrader = AutoBot(trader)
    algorithm = average_candle.AvgCandle(autoTrader)
    autoTrader.start(algorithm)

