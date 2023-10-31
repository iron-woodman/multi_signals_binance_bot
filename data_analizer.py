## -*- coding: utf-8 -*-
import time
import os
import src.logger as custom_logging
from src.pattern_hammer import HammerPattern
from src.pattern_big_candle import BigCandlePattern
from src.db import get_candles
from avg_volumes_updater import load_avg_volume_params
from src.config_handler import SPOT_AVG_VOLUMES_FILE, FUT_AVG_VOLUMES_FILE


def load_last_rec_id(filename):
    if os.path.isfile(filename) is False:
        return 0
    try:

        with open(filename, 'r', encoding='utf-8') as f:
            last_id = f.read()
            return int(last_id)
    except Exception as e:
        custom_logging.error(f"load_last_rec_id exception: {e}")
        return 0


def store_rec_id(filename, rec_id):
    """
    store last last recorf id to file
    :param filename:
    :param rec_id:
    :return:
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(rec_id))
def main():

    spot_avg_volumes = load_avg_volume_params(SPOT_AVG_VOLUMES_FILE)
    fut_avg_volumes = load_avg_volume_params(FUT_AVG_VOLUMES_FILE)

    last_spot_rec_id = load_last_rec_id('data/spot_5m_rec_id.txt')
    last_fut_rec_id = load_last_rec_id('data/fut_5m_rec_id.txt')
    hammer = HammerPattern()
    big_candle = BigCandlePattern()

    while True:
        fut_records = get_candles(last_fut_rec_id, 'fut_5m')
        spot_records = get_candles(last_spot_rec_id, 'spot_5m')
        # print('spot records: ', len(spot_records))
        # print('fut records: ', len(fut_records))
        hammer_spot_signal_list = []
        hammer_fut_signal_list = []
        big_candle_spot_signal_list = []
        big_candle_fut_signal_list = []

        # process  futures candles
        if len(fut_records) > 0:
            for row in fut_records:
                if int(row[0]) > last_fut_rec_id:
                    last_fut_rec_id = int(row[0])
                    avg_volume = 0
                    if row[1] in fut_avg_volumes:
                        avg_volume = fut_avg_volumes[row[1]]['5m']
                #     check for hammer pattern
                hammer_signal = hammer.check_bar_for_signal(
                    row[1], float(row[3]), float(row[6]), float(row[5]), float(row[6]), float(row[4]), '5m', row[2],
                    avg_volume)
                if hammer_signal != '':
                    hammer_fut_signal_list.append(hammer_signal)
                #     check for hammer pattern
                big_candle_signal = big_candle.check_bar_for_signal(
                    row[1], float(row[3]), float(row[6]), float(row[5]), float(row[6]), float(row[4]), '5m', row[2],
                    avg_volume)
                if big_candle_signal != '':
                    big_candle_fut_signal_list.append(big_candle_signal)
            print('fut hummer signals:\n', hammer_fut_signal_list)
            print('fut big candle signals:\n', big_candle_fut_signal_list)

            store_rec_id('data/fut_5m_rec_id.txt', last_fut_rec_id)# save last rec id to file

        # process spot candles
        if len(spot_records) > 0:
            for row in spot_records:
                if int(row[0]) > last_spot_rec_id:
                    last_spot_rec_id = int(row[0])
                    avg_volume = 0
                    if row[1] in spot_avg_volumes:
                        avg_volume = spot_avg_volumes[row[1]]['5m']
                #     check for big_canlde pattern
                hammer_signal = hammer.check_bar_for_signal(
                    row[1], float(row[3]), float(row[6]), float(row[5]), float(row[6]), float(row[4]), '5m', row[2], avg_volume)
                if hammer_signal != '':
                    hammer_spot_signal_list.append(hammer_signal)
                #     check for big_canlde pattern
                big_candle_signal = big_candle.check_bar_for_signal(
                    row[1], float(row[3]), float(row[6]), float(row[5]), float(row[6]), float(row[4]), '5m', row[2],
                    avg_volume)
                if big_candle_signal != '':
                    big_candle_spot_signal_list.append(big_candle_signal)
            print('spot hummer signals:\n', hammer_spot_signal_list)
            print('spot big candle signals:\n', big_candle_spot_signal_list)

            store_rec_id('data/spot_5m_rec_id.txt', last_spot_rec_id)# save last rec id to file


        time.sleep(10)

if __name__ == "__main__":
    main()