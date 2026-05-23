import psycopg2
from datetime import datetime, timezone

from src.config import settings
from src.transform.ohlcv import OhlcvCandle


def build_connection():
    return psycopg2.connect(
        host=settings.timescaledb_host,
        port=settings.timescaledb_port,
        user=settings.timescaledb_user,
        password=settings.timescaledb_password,
        dbname=settings.timescaledb_db,
    )


def write_candles(conn, candles: list[OhlcvCandle]) -> None:
    if not candles:
        return
    with conn.cursor() as cur:
        for candle in candles:
            window_start = datetime.fromtimestamp(candle.window_start / 1000, tz=timezone.utc)
            cur.execute(
                """
                INSERT INTO ohlcv_1m (symbol, window_start, open, high, low, close, volume, trade_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (symbol, window_start) DO UPDATE SET
                    high        = EXCLUDED.high,
                    low         = EXCLUDED.low,
                    close       = EXCLUDED.close,
                    volume      = EXCLUDED.volume,
                    trade_count = EXCLUDED.trade_count
                """,
                (
                    candle.symbol,
                    window_start,
                    str(candle.open),
                    str(candle.high),
                    str(candle.low),
                    str(candle.close),
                    str(candle.volume),
                    candle.trade_count,
                ),
            )
    conn.commit()
