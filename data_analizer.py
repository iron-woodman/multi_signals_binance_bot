## -*- coding: utf-8 -*-
import time
import os
import src.logger as custom_logging
from src.pattern_hammer import HammerPattern
from src.pattern_big_candle import BigCandlePattern
from src.db import get_candles
from avg_volumes_updater import load_avg_volume_params
from src.config_handler import SPOT_AVG_VOLUMES_FILE, FUT_AVG_VOLUMES_FILE, HAMMER_TLG_TOKEN, BIG_CANDLE_TLG_TOKEN, \
    HAMMER_TLG_CHANNEL_ID, BIG_CANDLE_TLG_CHANNEL_ID, TIMEFRAMES
from src.telegram_api import send_signal


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


    hammer = HammerPattern()
    big_candle = BigCandlePattern()

    while True:
        for timeframe in TIMEFRAMES:
            last_spot_rec_id = load_last_rec_id(f'data/spot_{timeframe}_rec_id.txt')
            last_fut_rec_id = load_last_rec_id(f'data/fut_{timeframe}_rec_id.txt')
            fut_records = get_candles(last_fut_rec_id, f'fut_{timeframe}')
            spot_records = get_candles(last_spot_rec_id, f'spot_{timeframe}')
            # print('spot records: ', len(spot_records))
            # print('fut records: ', len(fut_records))
            hammer_signals = dict()
            big_candle_signals = dict()
            avg_volume = 0

            # process  futures candles
            if len(fut_records) > 0:
                for row in fut_records:
                    if int(row[0]) <= last_fut_rec_id:
                        continue
                    last_fut_rec_id = int(row[0])
                    coin = row[1]
                    avg_volume = 0
                    if coin in fut_avg_volumes:
                        avg_volume = fut_avg_volumes[coin][timeframe]
                    #     check for hammer pattern
                    hammer_signal = hammer.check_bar_for_signal(
                        coin, float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), timeframe,
                        row[2], avg_volume)
                    if hammer_signal != '':
                        if coin in hammer_signals:
                            continue
                        hammer_signals[coin] = hammer_signal
                    #     check for hammer pattern
                    big_candle_signal = big_candle.check_bar_for_signal(
                        coin, float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), timeframe,
                        row[2], avg_volume)
                    if big_candle_signal != '':
                        if coin in big_candle_signals:
                            continue
                        big_candle_signals[coin] = big_candle_signal

                store_rec_id(f'data/fut_{timeframe}_rec_id.txt', last_fut_rec_id)  # save last rec id to file

            # process spot candles
            if len(spot_records) > 0:
                for row in spot_records:
                    if int(row[0]) <= last_spot_rec_id:
                        continue
                    last_spot_rec_id = int(row[0])
                    avg_volume = 0
                    coin = row[1]
                    if coin in spot_avg_volumes:
                        avg_volume = spot_avg_volumes[coin][timeframe]
                    #     check for big_canlde pattern
                    hammer_signal = hammer.check_bar_for_signal(
                        coin, float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), timeframe,
                        row[2], avg_volume)
                    if hammer_signal != '':
                        if coin in hammer_signals:
                            continue
                        hammer_signals[coin] = hammer_signal
                    #     check for big_canlde pattern
                    big_candle_signal = big_candle.check_bar_for_signal(
                        coin, float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), timeframe,
                        row[2], avg_volume)
                    if big_candle_signal != '':
                        if coin in big_candle_signals:
                            continue
                        big_candle_signals[coin] = big_candle_signal
                print('hummer signals:\n', hammer_signals)
                print('big candle signals:\n', big_candle_signals)

                store_rec_id(f'data/spot_{timeframe}_rec_id.txt', last_spot_rec_id)  # save last rec id to file



            hammer_common_signal = ''
            if len(hammer_signals) > 0:
                for coin in hammer_signals:
                    hammer_common_signal += hammer_signals[coin] + "\n\n"
                    if len(hammer_common_signal) > 3900:
                        send_signal(hammer_common_signal, HAMMER_TLG_TOKEN, HAMMER_TLG_CHANNEL_ID)
                        hammer_common_signal=''

            if len(hammer_common_signal) > 0:
                send_signal(hammer_common_signal, HAMMER_TLG_TOKEN, HAMMER_TLG_CHANNEL_ID)
                hammer_common_signal = ''

            big_candle_common_signal = ''
            if len(big_candle_signals) > 0:
                for coin in big_candle_signals:
                    big_candle_common_signal += big_candle_signals[coin] + "\n\n"
                    if len(big_candle_common_signal) > 3900:
                        send_signal(big_candle_common_signal, BIG_CANDLE_TLG_TOKEN, BIG_CANDLE_TLG_CHANNEL_ID)
                        big_candle_common_signal = ''

            if len(big_candle_common_signal) > 0:
                send_signal(big_candle_common_signal, BIG_CANDLE_TLG_TOKEN, BIG_CANDLE_TLG_CHANNEL_ID)

            time.sleep(10)


if __name__ == "__main__":
    main()
