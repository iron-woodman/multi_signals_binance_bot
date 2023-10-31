import json
from src.telegram_message import HummerTLGMessage
import src.logger as custom_logging
from src.pattern_base import CandlePattern


class HammerPattern(CandlePattern):
    def __init__(self):
        pass
    def check_bar_for_signal(self, symbol, open_, high, low, close, volume, timeframe, candle_time, avg_volume):
        super().check_bar_for_signal(symbol, open_, high, low, close, volume, timeframe, avg_volume)
        signal = ''
        try:
            hummer_direction = self.detect_hammer_patterns(open_, high, low, close, timeframe)
            proportion = self.get_candle_proportion(open_, high, low, close)
            volume_ratio = self.get_volume_ratio(volume, timeframe, symbol, avg_volume)
            if hummer_direction != '':
                tlg_message = HummerTLGMessage(symbol, timeframe, hummer_direction, proportion, volume_ratio)
                signal = tlg_message.generate_message()
                custom_logging.info(
                    f'{candle_time}:{symbol}:{hummer_direction}:' +
                    f'(open={open_}, high={high}, low={low}, close={close}, timeframe="{timeframe}")')
                # signal = f'{symbol}:{timeframe}:{hummer_direction}:{proportion}'
                # if volume_ratio is not None:
                #     signal += f'\nvolume: x {volume_ratio}'

        except Exception as e:
            print(e)
            custom_logging.error(f"check_bar_for_signal error: {e}.")
        return signal

    def get_volume_ratio(self, volume, timeframe, symbol, avg_volume):
        ratio = 0.0
        if avg_volume == 0:
            custom_logging.warning(f"Avg volume not exists for {symbol}:{timeframe}.")
            return None
        ratio = round(volume / avg_volume, 1)
        return ratio


    def detect_hammer_patterns(self, open, high, low, close, timeframe):
        signal = ''
        body_range = abs(open - close)
        total_range = high - low
        shadow_limit = 0.01  # 1 procent by default
        if timeframe == '4h':
            shadow_limit = 0.01
        elif timeframe == "1d":
            shadow_limit = 0.02
        elif timeframe == "1m":
            shadow_limit = 0.003
        elif timeframe == "5m":
            shadow_limit = 0.005

        try:

            if body_range * 3 < total_range:

                # ---------float zero division error correction
                if high == open:
                    high = open + 0.001 * open
                elif close == low:
                    low = close - close * 0.001
                elif high == close:
                    high = close + close * 0.001
                elif open == low:
                    low = open - open * 0.001
                # ---------------------------------------------

                if open > close:
                    # red hummers
                    if ((close - low) / total_range > 0.6) and (
                            close - low > shadow_limit * open) and \
                            ((close - low) / (high - open) >= 3):  # and ((close - low) / total_range < 0.2):
                        signal = 'LONG'
                    elif ((high - open) / total_range > 0.6) and (
                            high - open > shadow_limit * open) and (
                            (high - open) / (close - low) >= 3):  # and ((high - open) / total_range < 0.2):
                        signal = 'SHORT'

                else:
                    # green hummers
                    if ((open - low) / total_range > 0.6) and (open - low > shadow_limit * open) \
                            and ((open - low) / (high - close) >= 3):
                        signal = 'LONG'
                    elif ((high - close) / total_range > 0.6) and (
                            high - close > shadow_limit * open) and (
                            (high - close) / (open - low) >= 3):  # and ((high - open) / total_range < 0.2):
                        signal = 'SHORT'
        except Exception as e:
            custom_logging.error(f"detect_hammer_patterns error: {e}")
        return signal

    def get_candle_proportion(self, open_, high, low, close):
        if open_ == close:
            open_ = open_ + open_ * 0.0001
        proportion = round((high - low) / abs(open_ - close), 2)
        if 2 < proportion <= 2.5:
            return "1 to 2"
        elif 2.5 < proportion <= 3:
            return "1 to 3"
        elif 3 < proportion <= 3.5:
            return "1 to 3"
        elif 3.5 < proportion <= 4:
            return "1 to 4"
        elif 4 < proportion <= 4.5:
            return "1 to 4"
        elif 4.5 < proportion <= 5:
            return "1 to 5"
        elif 5 < proportion <= 5.5:
            return "1 to 5"
        elif 5.5 < proportion <= 6:
            return "1 to 6"
        elif 6 < proportion <= 6.5:
            return "1 to 6"
        elif 6.5 < proportion <= 7:
            return "1 to 7"
        elif 7 < proportion <= 7.5:
            return "1 to 7"
        elif 7.5 < proportion <= 8:
            return "1 to 8"
        elif 8 < proportion <= 8.5:
            return "1 to 8"
        elif 8.5 < proportion <= 9:
            return "1 to 9"
        elif 9 < proportion <= 9.5:
            return "1 to 9"
        elif 9.5 < proportion <= 10:
            return "1 to 10"
        elif 10 < proportion <= 10.5:
            return "1 to 10"
        else:
            return f"1 to {proportion}"

