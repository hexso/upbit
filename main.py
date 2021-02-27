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
        algorithm.start(trader)

    def _AutoTradeInit(self, trader):
        AutoBot.trader = trader
        f = open('private.txt', 'r')
        access_key = f.readline()
        private_key = f.readline()
        print('{} private_key is {}'.format(access_key, private_key))
        AutoBot.trader.login(access_key, private_key)

    def AnalyStart(self, analyzer):
        print()

    def GetBalance(self):
        return AutoBot.trader.GetBalance()

    def SendBuying(self, stockcode, amount, trade, price=None):
        result = AutoBot.trader.SendBuying(stockcode, amount, trade, price)
        result = result[0]
        self.notibot.SendMsg('매수: {}  총 개수 {}  총액 : {}원'.format(stockcode, result['executed_volume'], result['avg_price'] * result['executed_volume']))
        return result

    def SendSelling(self, stockcode, amount, trade, price=None):
        result = AutoBot.trader.SendBuying(stockcode, amount, trade, price)
        result = result[0]
        self.notibot.SendMsg('매도: {}  총 개수 {}  총액 : {}원'.format(stockcode, result['executed_volume'], result['avg_price'] * result['executed_volume']))
        return result

    def GetStocksList(self, money='KRW'):
        return AutoBot.trader.GetStocksList(money)

    def GetDayCandle(self, stockcode):
        return AutoBot.trader.GetDayCandle(stockcode)

    def GetMinCandle(self, stockcode, mins='1', count=1):
        return AutoBot.trader.GetMinCandle(stockcode, mins, count)

    def GetCurrentPrice(self, stockcode):
        return AutoBot.trader.GetCurrentPrice(stockcode)

    def CancelOrder(self, uuid):
        return AutoBot.trader.CancelOrder(uuid)

    @staticmethod
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
        algorithm = average_candle.AvgCandle()
        autoTrader.AutoStart(algorithm, trader)

    elif ch == 2:
        inspector = Inspector()
        inspector.Start()
    else :
        print('wrong choice')
        autoTrader.help()

