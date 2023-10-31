## -*- coding: utf-8 -*-
# collect candles into database
from src.websocket_handler import QueueManager
from src.binance_api import load_spot_list
from src.config_handler import TIMEFRAMES


if __name__ == '__main__':
    spot_list = load_spot_list()
    manager_spot = QueueManager(symbols=spot_list, timeframes=TIMEFRAMES, isSPOT=True)
    manager_spot.join()
