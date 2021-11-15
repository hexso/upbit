'''
거래량이 높고 변화폭이 심한 Coin들을 찾아 거래한다.
'''
import time

class BoxTrade:

    def __init__(self):
        self.trader = None
        self.USING_COIN_CNT = 5
        self.BUYING_PRICE = 100000
        self.coin_amount={}


    def SelectCoin(self):
        '''
        거래할 코인을 선택
        BTC마켓에서 고른다.
        매물대가 KRW는 너무 높다.
        틱 퍼센티지가 제일 높은 Coin들 5개 중 거래량이 높은걸 선택한다.
        '''
        stock_list = self.trader.GetStocksList('BTC')
        coin_list = []
        selected_coin = []
        for stock in stock_list:
            current_price = self.trader.GetCurrentPrice(stock)
            coin_list.append([stock,current_price])
            time.sleep(0.05)
        coin_list = sorted(coin_list, key=(lambda k: k[1]))
        for stock, price in coin_list:
            order_book = trader.GetOrderBook(stock)
            units = order_book[0]['orderbook_units']
            buy_volume = units[0]['ask_price'] * units[0]['ask_size']
            sell_volume = units[0]['bid_price'] * units[0]['bid_size']
            if buy_volume < 1 and sell_volume < 1:
                selected_coin.append(stock)
            time.sleep(0.05)

        return selected_coin


    def start(self, trader):
        self.trader = trader
        selected_coin = self.SelectCoin()
        print(selected_coin)



if __name__ == '__main__':
    import upbit
    from main import AutoBot
    autoTrader = AutoBot()
    trader = upbit.UpbitTrade()
    algorithm = BoxTrade()
    autoTrader.AutoStart(algorithm, trader)
