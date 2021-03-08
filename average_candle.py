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
        self.SEED_MONEY = 6000
        self.CANDLE_MIN = 10 # 분봉
        self.MAX_COIN_CNT = 20 # 탐색하는 코인 개수
        self.YIELD = 5# 목표 수익률
        self.UP_AVG_CANDLE = 15 + 1 # 상위 이동평균선 뒤에 + 1 은 바로 전 이동평균선을 보기 위함
        self.DOWN_AVG_CANDLE = 5 # 하위 이동평균선

        print('AvgCandle initiate')
        self.trader = None
        self.coin_candle_list = dict() # key값은 코인, value값은 self.UP_AVG_CANDLE + 1 크기의 리스트다.
        self.coin_amount = dict()
        self.coin_price = dict()
        self.selected_coin = list()
        self.total_money = 0
    def TargetCoin(self, coin):
        '''
        :param coin: 원하는 코인을 설정할 수 있다. 보통 리스트로 넘겨준다. 한개일 경우는 그냥 준다.
        :return:
        '''

        if type(list()) == type(coin):
            self.selected_coin = coin
        else:
            self.selected_coin.append(coin)

    def start(self, trader):
        self.trader = trader
        if not len(self.selected_coin):
            self.selected_coin = self.SelectCoin()

        for i in self.selected_coin:
            self.coin_amount[i] = 0
        balance = self.trader.GetBalance()
        sleep(1)
        for i in balance:
            self.coin_amount['KRW-' + i['currency']] = i['balance']
            self.coin_price['KRW-' + i['currency']] = i['avg_buy_price']
        print('selected coin is {}'.format(self.selected_coin))


        #처음 분봉 업데이트
        self.GetAvgCandle()
        while 1:
            for i in self.selected_coin:

                if self.coin_amount[i] == 0: # coin을 가지고 있지 않은 경우
                    res = self.CheckCross(self.coin_candle_list[i])
                    if res == 1:
                        print('{} coin을 구매하였습니다.'.format(i))
                        self.BuyCoinLimit(i)
                        print(self.coin_amount[i])


                else: # 코인을 가지고 있는 경우
                    res = self.CheckCross(self.coin_candle_list[i])
                    if res == 2:
                        print('데드크로스로 {} coin을 판매하였습니다.'.format(i))
                        result = self.SellCoinLimit(i)
                    else:
                        sleep(1)
                        price = self.trader.GetCurrentPrice(i)
                        profit = ((price - self.coin_price[i])/self.coin_price[i])*100
                        if profit > self.YIELD:
                            print('수익률 {} coin을 판매하였습니다. 수익률 : {}%'.format(i, profit))
                            result = self.SellCoinLimit(i)

    def CheckCross(self, avg_candle):
        '''
        참조 : self.UP_AVG_CANDLE, self.DOWN_AVG_CANDLE
        :param: avg_candle 총 self.UP_AVG_CANDLE만큼의 list
        :return:아래에 해당되지 않는 경우는 0
                골든 크로스(낮은 이동평균선이 높은 이동평균선을 뚫고 올라간 경우) 1
                데드 크로스(낮은 이동평균선이 높은 이동평균선을 뚫고 내려간 경우) 2

        '''
        before_low_avg = sum(avg_candle[1:self.DOWN_AVG_CANDLE + 1]) / self.DOWN_AVG_CANDLE
        now_low_avg = sum(avg_candle[:self.DOWN_AVG_CANDLE]) / self.DOWN_AVG_CANDLE

        before_high_avg = sum(avg_candle[1:self.UP_AVG_CANDLE]) / (self.UP_AVG_CANDLE - 1)
        now_high_avg = sum(avg_candle[:self.UP_AVG_CANDLE -1]) / (self.UP_AVG_CANDLE - 1)

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
            print('{} coin candle를 받아옵니다.'.format(i))
            result = self.trader.GetDayCandle(i)[0]
            tmp_dict[i] = result['candle_acc_trade_price']
            sleep(0.1)
        tmp_dict = sorted(tmp_dict.items(), reverse=True, key=lambda item: item[1])
        selected_coin = [i[0] for i in tmp_dict]
        return selected_coin[:self.MAX_COIN_CNT]

    def GetAvgCandle(self):
        '''
        :param 실시간으로 selected coin 리스트에 있는 코인들의 분봉을 얻는다.
        '''
        # 코인 동기화
        print('Avg Candle 받아 올 예정입니다.')
        tmp_list = list()
        for i in self.selected_coin :
            candle_dict = self.trader.GetMinCandle(i, self.CANDLE_MIN, self.UP_AVG_CANDLE)
            self.coin_candle_list[i] = [i['trade_price'] for i in candle_dict]
            sleep(self.TICK_WAITTIME)
        threading.Timer(self.CANDLE_MIN * 60, self.GetAvgCandle).start()

    def BuyCoinLimit(self, coin):
        '''
        self.SEED_MONEY를 고려해서 해당 코인을 일정 개수만큼산다.
        :param coin:
        :return:
        '''
        result = self.trader.SendBuying(coin, self.SEED_MONEY, '시장가')
        sleep(1)
        balance = self.trader.GetBalance()
        for i in balance:
            if i['currency'] == coin[4:]:
                self.coin_amount[coin] = float(i['balance'])
                self.coin_price[coin] = float(i['avg_buy_price'])
                break
        if self.coin_amount[coin] == 0:
            print(coin)
            print(i)
            print(balance)
            raise Exception('뭔가 이상함')

        return result

    def SellCoinLimit(self, coin):
        amount = self.coin_amount[coin]
        result = self.trader.SendSelling(coin, amount, '시장가')
        sleep(1)
        balance = self.trader.GetBalance()
        self.coin_amount[coin] = 0

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
    pass