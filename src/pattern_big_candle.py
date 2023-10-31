import json
from src.telegram_message import BigCandleTLGMessage
import src.logger as custom_logging
from src.pattern_base import CandlePattern
from config_handler import CANDLE_BODY_SIZE


class BigCandlePattern(CandlePattern):
    def __init__(self):
        pass
    def check_bar_for_signal(self, symbol, open_, high, low, close, volume, timeframe, avg_volume):
        super().check_bar_for_signal(symbol, open_, high, low, close, volume, timeframe, avg_volume)
        signal = ''
        bar_body_size = abs(open_ - close)
        bar_color = 'GREEN'
        if open_ >= close:
            bar_color = 'RED'
        price_move_size_procent = round(bar_body_size * 100 / open_, 2)
        if price_move_size_procent < CANDLE_BODY_SIZE:
            return
        volume_ratio = self.get_volume_ratio(volume, timeframe, symbol, avg_volume)
        custom_logging.info(
            f"{symbol}:{timeframe}:{bar_color}:PRICE_MOVE{price_move_size_procent}%:Vol. {volume_ratio}")
        tlg_message = BigCandleTLGMessage(symbol, timeframe, bar_color, price_move_size_procent, volume_ratio)
        signal = tlg_message.generate_message()
        custom_logging.info(
            f'{symbol}:{bar_color}:{price_move_size_procent}:' +
            f'(open={open_}, high={high}, low={low}, close={close}, timeframe="{timeframe}")')

        return signal
        # return f"{symbol}:{timeframe}:{price_move_size_percent}%"

    def get_volume_ratio(self, volume, timeframe, symbol, avg_volume):
        ratio = 0.0
        if avg_volume == 0:
            custom_logging.warning(f"Avg volume not exists for {symbol}:{timeframe}.")
            return None
        ratio = round(volume / avg_volume, 1)
        return ratio

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
