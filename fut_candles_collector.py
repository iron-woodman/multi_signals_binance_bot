## -*- coding: utf-8 -*-
# collect candles into database
from src.websocket_handler import QueueManager
from src.binance_api import load_futures_list
from src.config_handler import TIMEFRAMES


if __name__ == '__main__':
    futures_list = load_futures_list()
    manager_fut = QueueManager(symbols=futures_list, timeframes=TIMEFRAMES, isSPOT=False)
    manager_fut.join()