from abc import ABC, abstractmethod


class CandlePattern(ABC):
    @abstractmethod
    def check_bar_for_signal(self, symbol, open_, high, low, close, volume, timeframe, avg_volume):
        pass
        # print(f'{symbol}')
