import upbit
import average_candle
import sys
from predict_chart import Predict
from telegram_bot import TelegramBot
from inspect_chart import Inspector

class AutoBot:
    trader = None

    def __init__(self):
        self.PrintHelp()
        self.notibot = TelegramBot()

    def AutoStart(self, algorithm, trader):
        self._AutoTradeInit(trader)
        algorithm.start(AutoBot.trader)

    def _AutoTradeInit(self, trader):
        AutoBot.trader = trader
        with open('private.txt', 'r') as f:
            data = f.read()
            data = data.split('\n')
            for i in data:
                if 'accesskey' in i:
                    access_key = i[i.find(':')+1:]
                elif 'privatekey' in i:
                    private_key = i[i.find(':') + 1:]
                elif 'telegramtoken' in i:
                    token = i[i.find(':') + 1:]
                elif 'telegramchatid' in i:
                    chatid = i[i.find(':') + 1:]
            print('{} private_key is {}'.format(access_key, private_key))
            AutoBot.trader.Login(access_key, private_key)
            self.notibot.SetToken(token)
            self.notibot.SetChatId(chatid)

    def AnalyStart(self, analyzer):
        print()

    def GetBalance(self):
        return AutoBot.trader.GetBalance()

    def SendBuying(self, stockcode, amount, trade, price=None):
        result = AutoBot.trader.SendBuying(stockcode, amount, trade, price)
        result = result[0]
        self.notibot.SendMsg('매수: {}'.format(stockcode))
        return result

    def SendSelling(self, stockcode, amount, trade, price=None):
        result = AutoBot.trader.SendBuying(stockcode, amount, trade, price)
        result = result[0]
        self.notibot.SendMsg('매도: {}'.format(stockcode))
        return result

    def GetStocksList(self, money='KRW'):
        print('코인리스트를 받아옵니다.')
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
    def PrintHelp():
        print('자동 매매는 1, 차트 분석 및 알림은 2')

    def NotifyInfo(self, msg):
        self.notibot.SendMsg(msg)

if __name__ == '__main__':
    '''
    Upbit
    '''
    autoTrader = AutoBot()
    trader = upbit.UpbitTrade()
    algorithm = average_candle.AvgCandle()
    autoTrader.AutoStart(algorithm, trader)
    # ch = input('뭐할래?')
    # if ch == '1':
    #     trader = upbit.UpbitTrade()
    #     algorithm = average_candle.AvgCandle()
    #     autoTrader.AutoStart(algorithm, trader)
    #
    # elif ch == '2':
    #     inspector = Inspector()
    #     inspector.Start()
    # else :
    #     print('wrong choice')
    #     autoTrader.PrintHelp()

