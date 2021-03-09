from time import sleep
import threading

'''
실시간으로 코인들을 탐색하다가 갑자기 거래량이 급등함과 동시에 가격이 올라갔으면 매수한다.
'''

class RapidStock:

    def __init__(self):
        print('Rapid 탐색을 시작합니다.')
        self.trader = None
        self.MAX_COIN_CNT = 70 #탐색하는 코인수
        self.TICK_WAITTIME = 0.5
        self.SEED_MONEY = 10000
        self.CANDLE_AMOUNT = 2
        self.CANDLE_MIN = 1  # 분봉
        self.VOLUME_GAP = 3 # GAP의 배수만큼 증가되어있으면.
        self.YIELD = 1.5
        # 익절률
        self.LOSS_YIELD = -2 #손절률
        self.selected_coin = []
        self.coin_amount = dict()
        self.coin_price = dict()
        self.now_money = 0
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

    def start(self, trader):
        self.trader = trader
        self.selected_coin = self.SelectCoin()

        for i in self.selected_coin:
            self.coin_amount[i] = 0
        balance = self.trader.GetBalance()
        self.now_money = float(balance[0]['balance'])
        sleep(1)
        for i in balance:
            self.coin_amount['KRW-' + i['currency']] = float(i['balance'])
            self.coin_price['KRW-' + i['currency']] = float(i['avg_buy_price'])
        print('selected coin is {}'.format(self.selected_coin))

        while 1:
            for i in self.selected_coin:
                result = self.GetAvgCandle(i)
                sleep(self.TICK_WAITTIME)
                if self.coin_amount[i] == 0:
                    if result[0]['candle_acc_trade_volume'] > result[1]['candle_acc_trade_volume'] * self.VOLUME_GAP\
                            and result[0]['trade_price'] > result[1]['trade_price']\
                            and self.now_money > self.SEED_MONEY:
                        print('{} 코인을 구매합니다.'.format(i))
                        self.BuyCoinLimit(i)
                else:
                    profit = ((result[0]['trade_price'] - self.coin_price[i]) / self.coin_price[i]) * 100
                    if profit > self.YIELD:
                        self.SellCoinLimit(i)
                    elif profit < self.LOSS_YIELD:
                        self.SellCoinLimit(i)

    def GetAvgCandle(self, coin):
        '''
        :param 실시간으로 selected coin 리스트에 있는 코인들의 분봉을 얻는다.
        '''
        # 코인 동기화
        return self.trader.GetMinCandle(coin, self.CANDLE_MIN, self.CANDLE_AMOUNT)


    def BuyCoinLimit(self, coin):
        '''
        self.SEED_MONEY를 고려해서 해당 코인을 일정 개수만큼산다.
        :param coin:
        :return:
        '''
        result = self.trader.SendBuying(coin, self.SEED_MONEY, '시장가')
        sleep(self.TICK_WAITTIME)
        sleep(self.TICK_WAITTIME)
        balance = self.trader.GetBalance()
        self.now_money = float(balance[0]['balance'])
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
        sleep(self.TICK_WAITTIME)
        balance = self.trader.GetBalance()
        self.now_money = float(balance[0]['balance'])
        self.coin_amount[coin] = 0

        return result