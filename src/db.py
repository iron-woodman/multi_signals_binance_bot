

def store_candle(symbol, open_, high, low, close, volume, timeframe, isSPOT=False):
    db_name = ''
    if isSPOT:
        db_name = f'data/spot_{timeframe}.db'
    else:
        db_name = f'data/fut_{timeframe}.db'
    with open(db_name, 'a', encoding='utf-8') as f:
        f.write(f'{symbol},{open_},{high},{low},{close},{volume}')

