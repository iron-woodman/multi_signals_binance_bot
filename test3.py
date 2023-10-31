from binance.enums import HistoricalKlinesType
from binance import Client
from src.config_handler import BINANCE_API_KEY, BINANCE_Secret_KEY


client=Client(BINANCE_API_KEY, BINANCE_Secret_KEY)
fut_candles = client.get_historical_klines('BNBUSDT', Client.KLINE_INTERVAL_2HOUR, "1 day ago UTC",klines_type=HistoricalKlinesType.FUTURES)
spot_candles = client.get_historical_klines('BNBUSDT', Client.KLINE_INTERVAL_2HOUR, "1 day ago UTC",klines_type=HistoricalKlinesType.SPOT)

print("fut:\n",fut_candles)
print("spot:\n",spot_candles)
