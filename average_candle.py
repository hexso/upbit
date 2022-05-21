from time import sleep
import threading

import pandas as pd

from upbit_simulator import CoinSimulator
import coin_util
'''
10초 단위로 현재가를 얻어온다.
그래서 10초단위의 5평선, 15평선 두개를 기준으로
5평선이 15평선을 넘어섰을경우 매수
일정 이득률을 보면 매도한다.
5평선이 15평선을 뚫고 내려갈 경우도 매도한다.
거래대금이 높은 상위개수로만 돌린다.

Todo: 필요시 추가로 지정가 거래 구현 필요
'''

TARGET_COIN = ['KRW-BTC']

class AvgCandle:

    def __init__(self):
        self.TICK_WAITTIME = 0.1
        self.SEED_MONEY = 10000
        self.CANDLE_MIN = 15 # 분봉
        self.YIELD = 3# 목표 수익률
        self.UP_AVG_CANDLE = 30 # 상위 이동평균선
        self.MIDDLE_AVG_CANDLE = 15
        self.DOWN_AVG_CANDLE = 5 # 하위 이동평균선

        print('AvgCandle initiate')
        self.trader = None
        self.coin_candle_list = dict() # key값은 코인, value값은 self.UP_AVG_CANDLE + 1 크기의 리스트다.
        self.coin_amount = dict()
        self.coin_price = dict()
        self.selected_coin = TARGET_COIN
        self.buy_cnt = dict()

        for coin in self.selected_coin:
            self.coin_amount[coin] = 0
            self.coin_price[coin] = 0
            self.buy_cnt[coin] = 0

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

        for i in self.selected_coin:
            self.coin_amount[i] = 0
        sleep(1)

        #현재 잔고 불러오기
        balance = self.trader.GetBalance()
        for d in balance:
            coin_name = d['unit_currency'] + d['currency']
            if coin_name in self.selected_coin:
                self.coin_amount[coin_name] = d['balance']
                self.coin_price[coin_name] = d['avg_buy_price']
        print('selected coin is {}'.format(self.selected_coin))

        while 1:
            # 처음 분봉 업데이트
            self.GetAvgCandle()
            for i in self.selected_coin:
                if self.coin_amount[i] == 0: # coin을 가지고 있지 않은 경우
                    res = self.BuyingSignal(self.coin_candle_list[i])
                    if res == 1:
                        print('{} coin 구매 시그널 입니다.'.format(i))
                        self.BuyCoinLimit(i)


                else: # 코인을 가지고 있는 경우
                    res = self.SellingSignal(self.coin_candle_list[i])
                    now_coin_price = self.trader.GetCurrentPrice(i)
                    profit_rate = ((self.coin_price[i] - now_coin_price) / self.coin_price[i]) * 100
                    if res == 1 or profit_rate >= self.YIELD:
                        print('{} coin 판매 시그널입니다.'.format(i))
                        result = self.SellCoinLimit(i)
                    else:
                        if self.AverageDownSignal(self.coin_candle_list[i]) == 1:
                            print('{} coin 물타기 시그널 입니다.'.format(i))
                            self.BuyCoinLimit(i)

            sleep(self.CANDLE_MIN)

    def BuyingSignal(self, data):
        '''
        참조 : self.UP_AVG_CANDLE, self.DOWN_AVG_CANDLE
        :param: coin_util function을 통해 나온 데이터들
        5평선이 15,30평선을 뚫고 올라갈때 구매
        :return: 0(유지) 1(구매)
        '''
        now_data = data.loc[0]
        if now_data['ma' + str(self.DOWN_AVG_CANDLE)] > now_data['ma' + str(self.MIDDLE_AVG_CANDLE)] and \
            now_data['ma' + str(self.DOWN_AVG_CANDLE)] > now_data['ma' + str(self.UP_AVG_CANDLE)]:
            return 1
        return 0

    def SellingSignal(self, data):
        now_data = data.loc[0]
        if now_data['ma' + str(self.DOWN_AVG_CANDLE)] < now_data['ma' + str(self.MIDDLE_AVG_CANDLE)] and \
            now_data['ma' + str(self.DOWN_AVG_CANDLE)] < now_data['ma' + str(self.UP_AVG_CANDLE)]:
            return 1
        return 0

    def AverageDownSignal(self, data):
        return 0

    def GetAvgCandle(self):
        '''
        :param 실시간으로 selected coin 리스트에 있는 코인들의 분봉을 얻는다.
        '''
        # 코인 동기화
        print('Avg Candle 받아 올 예정입니다.')
        for i in self.selected_coin :
            data = self.trader.GetMinCandle(i, self.CANDLE_MIN, self.UP_AVG_CANDLE + 10)
            self.coin_candle_list[i] = coin_util.get_stock_indicators(data)
            sleep(self.TICK_WAITTIME)
        #threading.Timer(self.CANDLE_MIN * 60, self.GetAvgCandle).start()

    def BuyCoinLimit(self, coin):
        '''
        self.SEED_MONEY를 고려해서 해당 코인을 일정 개수만큼산다.
        :param coin:
        :return:
        '''
        result = self.trader.SendBuying(coin, self.SEED_MONEY, '시장가')
        result = result[0]
        sleep(1)
        if 'error' in result:
            print('{} 코인 구매를 시도하였으나 실패하였습니다.'.format(coin))
            print('에러 내용 : {}'.format(result))
            return result
        balance = self.trader.GetBalance()
        df = pd.DataFrame(balance)
        data = df.loc[df['currency'] == coin]
        self.coin_amount[coin] = data['balance']
        self.coin_price[coin] = data['avg_price']
        self.buy_cnt[coin] += 1
        print('코인 {}을 구매하였습니다. 총액 {}'.format(coin, result['paid_fee']))
        print('현재 해당 코인의 보유량은 총 {}원입니다.'.format(data['balance']*data['avg_price']))

        return result

    def SellCoinLimit(self, coin):
        amount = self.coin_amount[coin]
        result = self.trader.SendSelling(coin, amount, '시장가')
        sleep(1)
        result = result[0]
        balance = self.trader.GetBalance()
        df = pd.DataFrame(balance)
        if 'error' in result:
            print('{} 코인 판매를 시도하였으나 실패하였습니다.'.format(coin))
            print('에러 내용 : {}'.format(result))
            return result
        profit_price = (self.coin_price[coin] - result['avg_price']) * result['executed_volume']
        profit_rate = round((profit_price/(self.coin_amount[coin] * self.coin_price[coin]))*100,2)
        print('{} 코인을 판매하였습니다. 총 수익은 {}원, 수익률은 {}%입니다.'.format(coin, profit_price, profit_rate))
        self.buy_cnt[coin] = 1
        if df.loc[df['currency'] == coin].size == 0:
            self.coin_amount[coin] = 0
            self.coin_price[coin] = 0
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
    simulator = CoinSimulator(TARGET_COIN)
    simulator.InitGetAvgCandle(15, '2022-01-01 00:00:00','2022-05-20 00:00:00')
