import upbit
from notify.telegram_bot import TelegramBot
from rapid_stock import RapidStock
from buying_half import BuyingHalf
import average_candle
import upbit_simulator
import argparse
'''
매매하는 알고리즘은 start함수를 통해 실행된다.
나머지 매도, 매수같은 함수들은 아래의 함수들을 이용한다.
'''
COIN_LIST = ['KRW-BTC', 'KRW-ETH']

if __name__ == '__main__':
    '''
    Upbit
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--simul', action='store_true')
    parser.add_argument('--mute', action='store_true')
    args = parser.parse_args()

    algorithm = average_candle.AvgCandle()
    if args.simul is True:
        trader = upbit_simulator.CoinSimulator(COIN_LIST)
        average_candle.SIMULATOR = 1
        trader.InitGetAvgCandle(15,start_time='2022-01-01 00:00:00',end_time='2022-05-20 00:00:00')
    else:
        trader = upbit.UpbitTrade()
    algorithm.start(trader)
