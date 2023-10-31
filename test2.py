from binance import AsyncClient, BinanceSocketManager
import mysql.connector
import asyncio


async def main():
    api_key = '56uOhw46DIGjxJ5RMHkGMLi99DMfo73iOuB9ZAZgtxq1xfLRL2mDQKo6rEjOJXMS'
    api_secret = 'BKumF36wB6xjJau65zPTCRGIVU2Ak5VDr9XMQxCxaS73FYx0cn09WsbgDRIt43RT'
    client = await AsyncClient.create(api_key, api_secret)
    # get symbol details
    exchange_info = await client.get_exchange_info()
    futures_exchange_info = await client.futures_coin_exchange_info()

    # get spot and futures symbols from the exchange info
    spot_symbols = [symbol['symbol'] for symbol in exchange_info['symbols']]
    futures_symbols = [symbol['symbol'] for symbol in futures_exchange_info['symbols']]

    print('Spot Symbols: ')
    # get last 4h kline for each spot symbol
    for symbol in spot_symbols:
        if 'USDT' not in symbol: continue
        klines = await client.get_klines(symbol=symbol, interval=client.KLINE_INTERVAL_4HOUR)
        last_kline = klines[-1]
        print(f"{symbol}:SPOT: {last_kline}")

    print('Futures Symbols: ')
    # get last 4h kline for each futures symbol
    for symbol in futures_symbols:
        if 'USDT' not in symbol: continue
        klines = await client.futures_coin_klines(symbol=symbol, interval=client.KLINE_INTERVAL_4HOUR)
        last_kline = klines[-1]
        print(f"{symbol}:FUT: {last_kline}")

    print('Done')

# Python 3.7+
if __name__ == "__main__":
    asyncio.run(main())