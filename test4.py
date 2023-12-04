from binance import Client
from binance.enums import HistoricalKlinesType


def main():
    api_key = '56uOhw46DIGjxJ5RMHkGMLi99DMfo73iOuB9ZAZgtxq1xfLRL2mDQKo6rEjOJXMS'
    api_secret = 'BKumF36wB6xjJau65zPTCRGIVU2Ak5VDr9XMQxCxaS73FYx0cn09WsbgDRIt43RT'
    client = Client(api_key, api_secret)

    #pair = 'EGLDUSDT'
    pair = '1INCHUSDT'
    timeframe = '4h'
    st_time = "1 day ago UTC"

    bars = client.get_historical_klines(pair, timeframe, st_time, klines_type=HistoricalKlinesType.FUTURES)

    # for bar in bars:
    print('FUT: ', bars[-2])

    open_ = float(bars[-2][1])
    high = float(bars[-2][2])
    low = float(bars[-2][3])
    close = float(bars[-2][4])

    if open_ == close:
        open_ = open_ + open_ * 0.0001
    proportion = round((high - low) / abs(open_ - close), 2)

    print(proportion)

    #bars = client.get_historical_klines(pair, timeframe, st_time, klines_type=HistoricalKlinesType.SPOT)

    #print('SPOT: ',bars[-2])

    print('Done')

# Python 3.7+
if __name__ == "__main__":
    main()