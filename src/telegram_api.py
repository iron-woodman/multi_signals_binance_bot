## -*- coding: utf-8 -*-
import requests
from datetime import datetime
from config_handler import HAMMER_TLG_TOKEN, HAMMER_TLG_CHANNEL_ID, BIG_CANDLE_TLG_TOKEN, BIG_CANDLE_TLG_CHANNEL_ID
import time

import logger as custom_logging

signals_list = []
last_signal_time = 1.0


def send_signal(signal):
    print("*" * 30 + "\n" + signal)
    custom_logging.info("\n" + signal)
    url = "https://api.telegram.org/bot"
    url += TLG_TOKEN
    method = url + "/sendMessage"
    attemts_count = 5
    while (attemts_count > 0):
        r = requests.post(method, data={
            "chat_id": TLG_CHANNEL_ID,
            "text": signal,
            "parse_mode": "Markdown"
        })
        if r.status_code == 200:
            return
        elif r.status_code != 200:
            print(f'Telegram send signal error ({signal}). Status code={r.status_code}. Text="{r.text}".')
            custom_logging.error(f'Telegram send signal error:\n ({signal}). \nAttempts count={attemts_count}')
            datetime.time.sleep(1)
            attemts_count -= 1



def list_to_string(lst):
    mess = ''
    for item in lst:
        mess += '\n' + item + '\n'
    return mess


def send_signals_pack():
    global last_signal_time
    global signals_list
    while True:
        if time.time() - last_signal_time > 5:
            if len(signals_list) > 0:
                long_mess = list_to_string(signals_list)
                signals_list.clear()
                send_signal(long_mess)
                last_signal_time = time.time()
        time.sleep(1)


def add_signal_to_list(signal):
    global signals_list
    global last_signal_time

    signals_list.append(signal)
    last_signal_time = time.time()
