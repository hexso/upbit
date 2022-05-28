import talib
import pandas as pd


def get_stock_indicators(x):
    copied = x.copy()
    copied['ma5'] = talib.MA(copied['close'], 5)
    copied['ma15'] = talib.MA(copied['close'], 15)
    copied['ma30'] = talib.MA(copied['close'], 30)
    return copied.fillna(0)

if __name__ == '__main__':
    pass