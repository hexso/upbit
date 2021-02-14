from time import sleep

class Inspector:

    def __init__(self, trader, notifier):
        self.trader = trader
        self.notifier = notifier
        self.WAITTIME = 0.1
        self.MINS = 15
        self.CONSIDERCOUNT = 10
        self.TIME_TERM = 15 * 60 #(분)
        self.last_notice_time = {}
        self.stock_list = []

    def Start(self):
        self._CheckRapidDownChart()

        while 1:
            self.CheckRapidDownChart()

    def _CheckRapidDownChart(self):
        self.stock_list = self.GetCoinList()
        for i in self.stock_list:
            self.last_notice_time[i] = 0

    def CheckRapidDownChart(self):
        for i in self.stock_list:
            candle_list = self.GetMinCandle()
            max_price = self.CalcMaxPriWithDict(candle_list)
            now_price = self.trader.getCurrentPrice(self.selectedCoin)
            if max_price * 0.95 > now_price:
                self.notifier.SendMsg()
            print('coin is {} and now_price is {} max_price is {}'.format(i, now_price, max_price))
            sleep(self.WAITTIME)

    def CalcMaxPriWithDict(self, stock_list):
        '''
        :param stockList: 리스트 안에 dict들. opening_price, high_price, low_price, trade_price
        :return: 제일 큰 고가 금액
        '''
        max_price = 0
        for i in stock_list:
            high_price = int(i['high_price'])
            if max_price < high_price:
                max_price = high_price
        return max_price

    def GetMinCandle(self, stock_code, mins, count):
        min_candle = self.trader.getMinCandle(stock_code, mins, count)
        sleep(self.WAITTIME)
        return min_candle

    def GetCoinList(self):
        stock_list = self.trader.getStocksList()
        return stock_list