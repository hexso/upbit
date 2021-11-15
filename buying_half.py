'''
일정 비율 이상 떨어질때 마다 현재 구매량 만큼 추가매수를 한다.
그럼 평단가가 현재 마이너스 퍼센트의 절반이 된다.
매도의 경우 일정비율이상일 경우 매도를 한다.
'''
import time
class BuyingHalf:

    def __init__(self):
        self.trader = None
        self.USING_COIN_CNT = 5
        self.BUYING_PRICE = 100000
        self.BUYING_RATE = 5
        self.HALF_BUYING_RATE = 4
        self.SELLING_RATE = 5
        self.coin_amount = {}


    def SelectCoin(self):
        '''
        거래할 코인을 선택.
        하루평균 변화량이 큰 코인을 선택.
        '''
        stock_list = self.trader.GetStocksList()
        coin_list = []

        for stock in stock_list:
            candle_list = self.trader.GetMinCandle(stock,'3',100)
            most_high = max(candle_list, key = (lambda k : k['high_price']))['high_price']
            most_low = max(candle_list, key = (lambda k: k['low_price']))['low_price']
            change_rate = round((most_high-most_low)/most_high * 100, 4)
            coin_list.append([stock, change_rate])
            time.sleep(0.05)
        coin_list=sorted(coin_list, key = (lambda k : k[1]), reverse=True)
        print(coin_list)
        coin_list = [stock for stock,price in coin_list]
        return coin_list

    def start(self, trader):
        self.trader = trader
        selected_coin = self.SelectCoin()

        for coin in selected_coin:
            self.coin_amount[coin] = {'avg_price':0,'amount':0,'buy_cnt':0}

        print('매매할 코인 : ', selected_coin)
        exit(1)
        while 1:
            for coin in selected_coin:
                current_price=self.trader.GetCurrentPrice()
                if self.coin_amount[coin]['buy_cnt'] == 0:
                    #최근 1분봉 30개를 기준으로 현재가격이 최고점 대비 몇퍼센트 이상일 경우만 매수한다.
                    candle_list = self.trader.GetMinCandle(coin,'1',30)
                    most_high = max(candle_list, key=(lambda k: k['high_price']))['high_price']
                    if ((most_high-current_price)/most_high*100) > self.BUYING_RATE:
                        result = self.trader.SendBuying(coin, self.BUYING_PRICE,'시장가')
                        self.coin_amount[coin]['avg_price'] = result['avg_price']
                        self.coin_amount[coin]['amount'] = result['executed_volume']
                        self.coin_amount[coin]['buy_cnt'] = 1
                else:
                    now_chage_rate = round((current_price-self.coin_amount['avg_price'])/current_price * 100)
                    if now_chage_rate > self.SELLING_RATE:
                        #만약 이익퍼센트보다 높아졌을경우 익절한다.
                        self.trader.SendSelling(coin, self.coin_amount['amount'],'시장가')
                        self.coin_amount[coin]['avg_price'] = 0
                        self.coin_amount[coin]['amount'] = 0
                        self.coin_amount[coin]['buy_cnt'] = 0

                    elif now_chage_rate < -self.HALF_BUYING_RATE:
                        #물타기는 최대 2번까지.
                        #물타기 rate보다 떨어졌을경우 물타기를 시도한다.
                        if self.coin_amount['buy_cnt'] < 2:
                            self.trader.SendBuying(coin, self.BUYING_PRICE, '시장가')
                            result = self.trader.GetBalance(coin)
                            self.coin_amount[coin]['avg_price'] = result['avg_buy_price']
                            self.coin_amount[coin]['amount'] = result['balance']
                            self.coin_amount[coin]['buy_cnt'] =  self.coin_amount[coin]['buy_cnt'] + 1




if __name__ == '__main__':
    import upbit
    from main import AutoBot
    autoTrader = AutoBot()
    trader = upbit.UpbitTrade()
    algorithm = BuyingHalf()
    autoTrader.AutoStart(algorithm, trader)






