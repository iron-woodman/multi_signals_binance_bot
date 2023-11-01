## -*- coding: utf-8 -*-
import multiprocessing
import json
import os
import time
from binance import Client
from binance.enums import HistoricalKlinesType
from datetime import datetime
from src.binance_api import load_futures_list, load_spot_list
from src.config_handler import TIMEFRAMES, FUT_AVG_VOLUMES_FILE, SPOT_AVG_VOLUMES_FILE, BINANCE_API_KEY, BINANCE_Secret_KEY
import src.logger as custom_logging


THREAD_CNT = 2 # 3 потока на ядро
PAUSE = 5 # пауза между запросами истории
DEBUG = False# флаг вывода отладочных сообщений во время разработки

spot_list=[]
futures_list=[]

def GetVolumeListAndAvg(bars):
    _ = []
    avg = 0.0
    for bar in bars:
        val = float(bar[5])
        _.append(val)
        avg += val
    avg = avg/len(bars)
    return avg


def load_history_bars(task):
    """
    Load historical bars
    :return:
    """
    result = dict()
    pair = task[0]
    api_key = task[1]
    secret_key = task[2]
    all_timeframes = task[3]
    is_spot = task[4]
    client = Client(api_key, secret_key)

    try:
        result['id'] = pair
        for timeframe in all_timeframes :

            if timeframe == '1m':
                st_time = "1 day ago UTC"
            elif timeframe == '5m':
                st_time = "5 day ago UTC"
            elif timeframe == '10m':
                st_time = "5 day ago UTC"
            elif timeframe == '15m':
                st_time = "5 day ago UTC"
            elif timeframe == '30m':
                st_time = "5 day ago UTC"
            elif timeframe == '1h':
                st_time = "2 day ago UTC"
            elif timeframe == '2h':
                st_time = "2 day ago UTC"
            elif timeframe == '4h':
                st_time = "4 day ago UTC"
            elif timeframe == '1d':
                st_time = "20 day ago UTC"
            else:
                print('Unknows timeframe:', timeframe)
                custom_logging.error(f'load history bars error: unknown timeframe "{timeframe}"')
                continue

            bars = []
            try:
                if is_spot:
                    bars = client.get_historical_klines(pair, timeframe, st_time, klines_type=HistoricalKlinesType.FUTURES)
                else:
                    bars = client.get_historical_klines(pair, timeframe, st_time, klines_type=HistoricalKlinesType.SPOT)

            except Exception as e:
                print(pair,':', e)

            if len(bars) == 0:
                print(f" 0 bars has been gethered from server. client.get_historical_klines({pair}, {timeframe}, "
                      f"{st_time})")
                result[timeframe] = 0
                continue
            avg = GetVolumeListAndAvg(bars)
            result[timeframe] = round(avg, 2) #float("{0.2f}".format(avg))
        print(result)
        time.sleep(PAUSE)
        return result
    except Exception as e:
        print("Exception when calling load_history_bars: ", e)

        return None


def load_futures_history_bars_end(responce_list):
    data = dict()
    for responce in responce_list:
        id = responce['id']
        del responce['id']
        data[id] = responce
    # print(data)
    try:
        with open(FUT_AVG_VOLUMES_FILE, 'w', encoding='cp1251') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, separators=(',', ': '))
            print('Futures avg volumes stored to file')
            custom_logging.info('Futures avg volumes stored to file')


        avg_volumes = load_avg_volume_params(FUT_AVG_VOLUMES_FILE)
    except Exception as e:
        print("Futures avg volumes loading exception:", e)
        custom_logging.error(f'Futures avg volumes loading exception: {e}')


def load_spot_history_bars_end(responce_list):
    data = dict()
    for responce in responce_list:
        id = responce['id']
        del responce['id']
        data[id] = responce
    # print(data)
    try:
        with open(SPOT_AVG_VOLUMES_FILE, 'w', encoding='cp1251') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, separators=(',', ': '))
            print('Spot avg volumes stored to file')
            custom_logging.info('Spot avg volumes stored to file')


        avg_volumes = load_avg_volume_params(SPOT_AVG_VOLUMES_FILE)
    except Exception as e:
        print("Spot avg volumes loading exception:", e)
        custom_logging.error(f'Spot avg volumes loading exception: {e}')


def load_avg_volume_params(file):
    if os.path.isfile(file) is False: # file not exists
        print(f'Avg volumes file  "{file}" not exists.')
        return None
    pairs = []
    try:
        with open(file, 'r', encoding='cp1251') as f:
            avg_volumes = json.load(f)
        print('Volumes loaded.')
        return avg_volumes
    except Exception as e:
        print("load_avg_volume_params exception:", e)
        return None


def update_avg_volumes(timeframes, is_spot=False):
    tasks = []


    try:
        if is_spot:
            custom_logging.info('Spot AVG volumes update started...')

            for symbol in spot_list:
                tasks.append((symbol, BINANCE_API_KEY, BINANCE_Secret_KEY, timeframes, is_spot))

            with multiprocessing.Pool(multiprocessing.cpu_count() * THREAD_CNT) as pool:
                pool.map_async(load_history_bars, tasks, callback=load_spot_history_bars_end)
                pool.close()
                pool.join()
        else:
            custom_logging.info('Futures AVG volumes update started...')
            for symbol in futures_list:
                tasks.append((symbol, BINANCE_API_KEY, BINANCE_Secret_KEY, timeframes, is_spot))

            with multiprocessing.Pool(multiprocessing.cpu_count() * THREAD_CNT) as pool:
                pool.map_async(load_history_bars, tasks, callback=load_futures_history_bars_end)
                pool.close()
                pool.join()
    except Exception as ex:
        print("update_avg_volumes exception:", ex)
        custom_logging.error(f"update_avg_volumes exception: {ex}")
        return



# def load_futures_list():
#     client = Client(BINANCE_API_KEY, BINANCE_Secret_KEY)
#     futures_info_list = client.futures_exchange_info()
#     futures = []
#     for item in futures_info_list['symbols']:
#         if item['status'] != 'TRADING': continue
#         futures.append(item['pair'])
#     return futures


def update_avg_volumes_by_time():
    while True:
        if datetime.now().hour == 2 and datetime.now().minute == 13:
            update_avg_volumes(TIMEFRAMES)
        time.sleep(60)


def main():
    global futures_list
    global spot_list
    futures_list = load_futures_list()
    spot_list = load_spot_list()

    if os.path.isfile(FUT_AVG_VOLUMES_FILE) is False:  # avg volumes file don't exists
        # get avg volumes for every timeframe
        update_avg_volumes(TIMEFRAMES)
    elif os.path.getsize(FUT_AVG_VOLUMES_FILE) == 0:
        update_avg_volumes(TIMEFRAMES)

    if os.path.isfile(SPOT_AVG_VOLUMES_FILE) is False:  # avg volumes file don't exists
        # get avg volumes for every timeframe
        update_avg_volumes(TIMEFRAMES, True)
    elif os.path.getsize(SPOT_AVG_VOLUMES_FILE) == 0:
        update_avg_volumes(TIMEFRAMES, True)



if __name__ == '__main__':
    main()