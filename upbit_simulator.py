'''
실제 시뮬레이션 하기 전, 과거 데이터들로 시뮬레이션을 하기 위한 코드
'''
import upbit
from datetime import datetime, timedelta
from time import sleep
class CoinSimulator:
    '''
    upbit를 이용하여 데이터를 수집한다.
    '''
    def __init__(self, selected_coin):
        '''
        :param selected_data: 시뮬레이션을 하기 위해 데이터를 미리 초기화시 선택해야 한다.
        현재 Candle만 구현할 예정
        '''
        self.SLEEP_TIME = 0.1

        self.selected_coin = selected_coin
        self.trader = upbit.UpbitTrade()
        self.coin_candle_data = dict()
        self.avg_index = dict()
        self.balance = list()
        for i in self.selected_coin:
            self.avg_index[i] = 50
            self.balance.append({'currency':i.split('-')[1],'balance':0, 'avg_price':0, 'unit_currency':'KRW'})

    def InitGetAvgCandle(self, time_tick, start_time, end_time):
        '''
        분봉 긁어오는 데이터
        :param time_tick: 몇분봉을 기준으로 할지 준다.
        :param start_time: 해당 날짜부터 긇어온다. yyyy-MM-dd HH:mm:ss 형식
        :param end_time:  이 날짜 까지 긇어온다. yyyy-MM-dd HH:mm:ss 형식
        :return: self.candle_list에 start_time부터 저장한다.
        '''
        start_time_format = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time_format = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        get_data_cnt = (end_time_format - start_time_format).total_seconds()/(60*time_tick)
        print('시작날짜 : {} 부터 {}까지 {}간격으로 크롤링할 예정입니다.'.format(start_time,end_time, time_tick))
        for coin in self.selected_coin:
            data = self.trader.GetMinCandle(coin, time_tick, get_data_cnt, end_time)
            print("{} 크롤링 완료".format(coin))
            self.coin_candle_data[coin] = data
        print('=====================모든 coin data 크롤링 완료=====================')

    def GetMinCandle(self, stockcode, mins='1', count=1, start_time = None):
        self.avg_index[stockcode] +=1
        index = self.avg_index[stockcode]
        if index >= len(self.coin_candle_data[stockcode]):
            return None
        return self.coin_candle_data[stockcode].iloc[index-count:index]

    def GetCurrentPrice(self, stockcode):
        index = self.avg_index[stockcode]
        return self.coin_candle_data[stockcode].iloc[index]['close']

    def GetBalance(self, coin=False):
        '''

        :return:
        '''
        return self.balance

    def SendBuying(self, stockcode, amount, trade, price=None):
        result = {}
        index = self.avg_index[stockcode]
        result['price'] = self.coin_candle_data[stockcode].iloc[index]['close']
        result['balance'] = amount / self.coin_candle_data[stockcode].iloc[index]['close']
        result['paid_fee'] = result['price'] * result['balance']
        for data in self.balance:
            if data['unit_currency']+'-'+data['currency'] == stockcode:
                self.balance.remove(data)
                total_price = data['avg_price']*data['balance']
                data['avg_price'] = round((total_price + result['paid_fee'])/(result['balance'] + data['balance']),2)
                data['balance'] += result['balance']
                self.balance.append(data)
                break

        return result


    def SendSelling(self, stockcode, amount, trade, price=None):
        result = {}
        index = self.avg_index[stockcode]
        result['trades'] = [{}]
        result['trades'][0]['price'] = self.coin_candle_data[stockcode].iloc[index]['close']
        result['volume'] = amount
        for data in self.balance:
            if data['unit_currency']+'-'+data['currency'] == stockcode:
                self.balance.remove(data)
                data['balance'] = 0
                data['avg_price'] = 0
                self.balance.append(data)
                break
        return result

if __name__ == '__main__':
    pass