from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OhlcvCandle:
    symbol: str
    window_start: int  # epoch ms, floored to the minute
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    trade_count: int


def _minute_bucket(trade_time_ms: int) -> int:
    return (trade_time_ms // 60_000) * 60_000


class OhlcvAccumulator:
    def __init__(self) -> None:
        self._windows: dict[tuple, OhlcvCandle] = {}

    def update(self, record: dict) -> tuple[list[OhlcvCandle], OhlcvCandle]:
        symbol = record["symbol"]
        trade_time = record["trade_time"]
        price = Decimal(record["price"])
        quantity = Decimal(record["quantity"])
        bucket = _minute_bucket(trade_time)
        key = (symbol, bucket)

        completed = [
            candle for k, candle in list(self._windows.items())
            if k[0] == symbol and k[1] < bucket
        ]
        for candle in completed:
            del self._windows[(candle.symbol, candle.window_start)]

        if key not in self._windows:
            self._windows[key] = OhlcvCandle(
                symbol=symbol,
                window_start=bucket,
                open=price,
                high=price,
                low=price,
                close=price,
                volume=quantity,
                trade_count=1,
            )
        else:
            candle = self._windows[key]
            candle.high = max(candle.high, price)
            candle.low = min(candle.low, price)
            candle.close = price
            candle.volume += quantity
            candle.trade_count += 1

        return completed, self._windows[key]
