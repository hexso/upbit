import upbit
import average_candle
import sys
from predict_chart import Predict
from telegram_bot import TelegramBot
from inspect_chart import Inspector

class AutoBot:
    trader = None

    def __init__(self):
        self.help()
        self.notibot = TelegramBot()

    def AutoStart(self, algorithm, trader):
        self._AutoTradeInit(trader)
        algorithm.start()

    def _AutoTradeInit(self,trader):
        AutoBot.trader = trader
        f = open('private.txt', 'r')
        accessKey = f.readline()
        privateKey = f.readline()
        print('{} privatekey is {}'.format(accessKey, privateKey))
        AutoBot.trader.login(accessKey, privateKey)

    def AnalyStart(self, analyzer):
        print()

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

    def getMinCandle(self, stockCode, mins='1', count=1):
        return AutoBot.trader.getMinCandle(stockCode, mins, count)

    def getCurrentPrice(self, stockCode):
        return AutoBot.trader.getCurrentPrice(stockCode)

    def CancelOrder(self, uuid):
        return AutoBot.trader.CancelOrder(uuid)

    def help(self):
        print('자동 매매는 1, 차트 분석 및 알림은 2')

    def NotifyInfo(self, msg):
        self.notibot.SendMsg(msg)

if __name__ == '__main__':
    '''
    Upbit
    '''
    autoTrader = AutoBot()
    ch = input()
    if ch == 1:
        trader = upbit.UpbitTrade()
        algorithm = average_candle.AvgCandle(autoTrader)
        autoTrader.AutoStart(algorithm, trader)

    elif ch == 2:
        inspector = Inspector()
        inspector.Start()
    else :
        print('wrong choice')
        autoTrader.help()

