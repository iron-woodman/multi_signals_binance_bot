import mysql.connector
from src.pattern_base import HammerPattern
from src.db import get_candles




fut_records = get_candles(0, 'fut_5m')
spot_records = get_candles(0, 'spot_5m')

print('spot records: ', len(spot_records))
print('fut records: ', len(fut_records))

hammer = HammerPattern()

fut_signal_list = []
for row in fut_records:
    hammer_signal = hammer.check_bar_for_signal(
        row[1], float(row[3]), float(row[6]), float(row[5]), float(row[6]), float(row[4]), '5m', row[2])
    # open,
    if hammer_signal != '':
        # print(signal)
        # send_signal(signal)
        fut_signal_list.append(hammer_signal)
print('fut hummer signals:\n', fut_signal_list)

spot_signal_list = []
for row in spot_records:
    hammer_signal = hammer.check_bar_for_signal(
        row[1], float(row[3]), float(row[6]), float(row[5]), float(row[6]), float(row[4]), '5m', row[2])
    # open,
    if hammer_signal != '':
        # print(signal)
        # send_signal(signal)
        spot_signal_list.append(hammer_signal)
print('spot hummer signals:\n', spot_signal_list)

