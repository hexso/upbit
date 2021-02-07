import upbit
import average_candle

class AutoBot():
    trader = None

    def __init__(self, trader):
        AutoBot.trader = trader
        f = open('private','r')
        accessKey = f.readline()
        privateKey = f.readline()
        AutoBot.trader.login(accessKey, privateKey)

    def start(self, algorithm):
        algorithm.start()

    def getBalance(self):
        return AutoBot.trader.getBalance()

    def sendBuying(self, stockCode, amount, trade, price=None):
        return AutoBot.trader.sendBuying(stockCode, amount, trade, price)

    def sendSelling(self, stockCode, amount, trade, price=None):
        return AutoBot.trader.sendSelling(self, stockCode, amount, trade, price)

    def getStocksList(self, money="KRW"):
        return AutoBot.trader.getStocksList(self, money)

    def getDayCandle(self, stockCode):
        return AutoBot.trader.getDayCandle(stockCode)

    def getMinCandle(self, stockCode):
        return AutoBot.trader.getMinCandle(stockCode)


if __name__ == '__main__':
    '''
    Upbit를 이용하여 거래
    '''
    trader = upbit.UpbitTrade()
    autoTrader = AutoBot(trader)
    algorithm = average_candle.AvgCandle()
    autoTrader.start(algorithm)

