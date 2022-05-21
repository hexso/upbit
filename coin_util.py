import talib
import pandas as pd


def get_stock_indicators(x):
    df = pd.DataFrame(x)
    df.columns = map(str.lower, df.columns)
    df = df.sort_values('candle_date_time_utc')
    df['ma5'] = talib.MA(df['trade_price'], 5)
    df['ma15'] = talib.MA(df['trade_price'], 15)
    df['ma30'] = talib.MA(df['trade_price'], 30)
    return df.fillna(0)

if __name__ == '__main__':
    pass