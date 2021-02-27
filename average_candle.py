from time import sleep
import threading
'''
10초 단위로 현재가를 얻어온다.
그래서 10초단위의 5평선, 15평선 두개를 기준으로
5평선이 15평선을 넘어섰을경우 매수
일정 이득률을 보면 매도한다.
5평선이 15평선을 뚫고 내려갈 경우도 매도한다.
거래대금이 높은 상위개수로만 돌린다.

Todo: 필요시 추가로 지정가 거래 구현 필요
'''



class AvgCandle:

    def __init__(self):
        self.TICK_WAITTIME = 0.1
        self.SEED_MONEY = 100000
        self.CANDLE_MIN = 10 # 분봉
        self.MAX_COIN_CNT = 15 # 탐색하는 코인 개수
        self.YIELD = 1 # 목표 수익률
        self.UP_AVG_CANDLE = 15 + 1 # 상위 이동평균선 뒤에 + 1 은 바로 전 이동평균선을 보기 위함
        self.DOWN_AVG_CANDLE = 5 # 하위 이동평균선

        print('AvgCandle initiate')
        self.trader = None
        self.coin_candle_list = dict() # key값은 코인, value값은 self.UP_AVG_CANDLE + 1 크기의 리스트다.
        self.coin_amount = dict()
        self.selected_coin = [0] * self.MAX_COIN_CNT

    def start(self, trader):
        self.trader = trader
        self.selected_coin = self.SelectCoin()
        for i in self.selected_coin:
            self.coin_amount[i] = 0
        print('selected coin is {}'.format(self.selected_coin))


        #처음 분봉 업데이트
        self.GetAvgCandle()

        #Thread로 코인가격 받아오기.
        threading.Timer(self.CANDLE_MIN, self.GetAvgCandle()).start()
        while 1:
            for i in self.selected_coin:

                if self.coin_amount[i] == 0: # coin을 가지고 있지 않은 경우
                    if self.CheckCross(self.coin_candle_list[i]) == 1:
                        result = self.BuyCoinLimit(i)


                else: # 코인을 가지고 있는 경우
                    if self.CheckCross(self.coin_candle_list[i]) == 2:
                        result = self.SellCoinLimit(i)

    def CheckCross(self, avg_candle):
        '''
        참조 : self.UP_AVG_CANDLE, self.DOWN_AVG_CANDLE
        :param: avg_candle 총 self.UP_AVG_CANDLE만큼의 list
        :return:아래에 해당되지 않는 경우는 0
                골든 크로스(낮은 이동평균선이 높은 이동평균선을 뚫고 올라간 경우) 1
                데드 크로스(낮은 이동평균선이 높은 이동평균선을 뚫고 내려간 경우) 2

        '''
        before_low_avg = avg_candle[1:self.DOWN_AVG_CANDLE + 1] / self.DOWN_AVG_CANDLE
        now_low_avg = avg_candle[:self.DOWN_AVG_CANDLE] / self.DOWN_AVG_CANDLE

        before_high_avg = avg_candle[1:self.UP_AVG_CANDLE -1] / (self.UP_AVG_CANDLE - 1)
        now_high_avg = avg_candle[:self.UP_AVG_CANDLE -1] / (self.UP_AVG_CANDLE - 1)

        if before_low_avg < before_high_avg and now_low_avg >= now_high_avg:
            return 1
        elif before_low_avg > before_high_avg and now_low_avg <= now_high_avg:
            return 2
        else:
            return 0


    def SelectCoin(self):
        '''
        volume이 큰 coin들을 선택.
        갯수는 총 self.MAX_COIN_CNT개
        :return: 코인을 리스트로 반환.
        '''
        stock_list = self.trader.GetStocksList()
        tmp_dict = dict()
        selected_coin = []
        for i in stock_list:
            result = self.trader.getDayCandle(i)
            tmp_dict[i] = result['candle_acc_trade_price']
            sleep(0.1)
        tmp_dict = sorted(tmp_dict.items())
        selected_coin = tmp_dict.keys()
        return selected_coin[:self.MAX_COIN_CNT]

    def GetAvgCandle(self):
        '''
        :param 실시간으로 selected coin 리스트에 있는 코인들의 분봉을 얻는다.
        '''
        # 코인 동기화
        tmp_list = list()
        for i in self.selected_coin :
            candle_dict = self.trader.GetMinCandle(i, self.CANDLE_MIN, self.UP_AVG_CANDLE)
            self.coin_candle_list[i] = [i['trade_price'] for i in candle_dict]
            sleep(self.TICK_WAITTIME)
        threading.Timer(self.CANDLE_MIN, self.GetAvgCandle).start()

    def BuyCoinLimit(self, coin):
        '''
        self.SEED_MONEY를 고려해서 해당 코인을 일정 개수만큼산다.
        :param coin:
        :return:
        '''
        price = self.trader.getCurrentPrice(coin)
        amount = int(self.SEED_MONEY/price)
        result = self.trader.SendBuying(coin, amount, '시장가')
        self.coin_amount[coin] = result['executed_volume']
        return result

    def SellCoinLimit(self, coin):
        amount = self.coin_amount[coin]
        result = self.trader.SendSelling(coin, amount, '시장가')
        self.coin_amount[coin] = result['remaining_volume']
        return result

    def checkBuy(self):
        pass

    def checkSell(self):
        pass

    def checkBalance(self):
        pass

    def CancelOrder(self):
        self.trader.CancelOrder(self.lastuuid)
        pass







if __name__ == '__main__':
    print('average algorithm')