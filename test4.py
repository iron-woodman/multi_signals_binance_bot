from binance import Client
from binance.enums import HistoricalKlinesType





def calculate_proportion(open_, high, low, close):
    if open_ == close:
        open_ = open_ + open_ * 0.0001
    if open_ >= close:
        up_shadow = high - open_
        low_shadow = close-low
    else:
        up_shadow = high - close
        low_shadow = open_ - low

    if up_shadow >= low_shadow:
        bigger_shadow = up_shadow
    else:
        bigger_shadow = low_shadow

    proportion = round(bigger_shadow / abs(open_ - close), 2)
    return proportion



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
    print('FUT: ', bars[-3])

    bar = bars[-3]
    open_ = float(bar[1])
    high = float(bar[2])
    low = float(bar[3])
    close = float(bar[4])

    proportion = calculate_proportion(open_, high, low, close)
    print(proportion)

    #bars = client.get_historical_klines(pair, timeframe, st_time, klines_type=HistoricalKlinesType.SPOT)

    #print('SPOT: ',bars[-2])

    print('Done')

# Python 3.7+
if __name__ == "__main__":
    main()