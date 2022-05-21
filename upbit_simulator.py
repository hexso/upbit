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
        for i in self.selected_coin:
            self.avg_index[i] = -1

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
        print('시작날짜 : {} 부터 {}까지 {}간격으로 크롤링할 예정입니다.'.format(start_time,end_time, time_tick))
        for coin in self.selected_coin:
            candle_list = list()
            while start_time_format < end_time_format:
                start_time_format = start_time_format + timedelta(minutes=time_tick * 200) # 업비트는 해당 날짜를 기준으로 과거 데이터를 갖고오기 때문에 미리 +를 해줘야 한다.
                start_time_str = start_time_format.strftime("%Y-%m-%d %H:%M:%S")
                candle_data = self.trader.GetMinCandle(coin, time_tick, 200, start_time_str)
                result = sorted(candle_data, key=lambda x: x['candle_date_time_kst'])
                candle_list.append(result)
                sleep(self.SLEEP_TIME)
            print("{} 크롤링 완료".format(coin))
            self.coin_candle_data[coin] = candle_list
        print('=====================모든 coin data 크롤링 완료=====================')
    def GetMinCandle(self, stockcode, mins='1', count=1, start_time = None):
        self.avg_index[stockcode] +=1
        return self.coin_candle_data[self.avg_index[stockcode]]
if __name__ == '__main__':
    pass