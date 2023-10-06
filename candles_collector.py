## -*- coding: utf-8 -*-
# collect candles into database

import logging
from binance import Client, ThreadedWebsocketManager
import mysql.connector

from src.websocket_handler import QueueManager
from src.binance_api import futures_list, spot_list
from src.config_handler import TIMEFRAMES, AVG_VOLUMES_FILE

api_key = '56uOhw46DIGjxJ5RMHkGMLi99DMfo73iOuB9ZAZgtxq1xfLRL2mDQKo6rEjOJXMS'
api_secret = 'BKumF36wB6xjJau65zPTCRGIVU2Ak5VDr9XMQxCxaS73FYx0cn09WsbgDRIt43RT'


class BinanceWebSocket(object):
    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.client_fut = Client(self.API_KEY, self.API_SECRET)
        self.client_fut.API_URL = 'https://fapi.binance.com/fapi'
        self.twm = ThreadedWebsocketManager(api_key=self.API_KEY, api_secret=self.API_SECRET)

        # Create MySQL connection
        self.conn = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )
        self.cursor = self.conn.cursor()

    def process_message(self, msg):
        print(f"message type: {msg['e']}")
        print(msg)

        # Assuming the table 'candles' exists with these columns: 'timestamp', 'open', 'high', 'low', 'close', 'volume'
        try:
            sql = '''
                INSERT INTO candles (timestamp, open, high, low, close, volume) 
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            self.cursor.execute(sql, (
            msg['k']['t'], msg['k']['o'], msg['k']['h'], msg['k']['l'], msg['k']['c'], msg['k']['v']))
            self.conn.commit()
        except Exception as e:
            # log any error
            logging.error(f'Error occurred: {e}')

    def start_socket_manager(self):
        # Start the threaded websocket manager
        self.twm.start()

        # Get futures exchange info
        futures = self.client_fut.futures_exchange_info()

        # Add futures to the websocket manager
        for future in futures['symbols']:
            self.twm.start_kline_futures_socket(symbol=future['symbol'], interval=self.client_fut.KLINE_INTERVAL_4HOUR,
                                                callback=self.process_message)


if __name__ == '__main__':
    # ws = BinanceWebSocket('your_api_key', 'your_secret')
    # ws.start_socket_manager()

    manager_fut = QueueManager(symbols=futures_list, timeframes=TIMEFRAMES)
    manager_fut.join()

    manager_spot = QueueManager(symbols=spot_list, timeframes=TIMEFRAMES)
    manager_spot.join()