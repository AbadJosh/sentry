CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE trades (
    trade_id        BIGINT       NOT NULL,
    event_type      TEXT         NOT NULL,
    event_time      TIMESTAMPTZ  NOT NULL,
    symbol          TEXT         NOT NULL,
    price           TEXT         NOT NULL,
    quantity        TEXT         NOT NULL,
    trade_time      TIMESTAMPTZ  NOT NULL,
    is_buyer_maker  BOOLEAN      NOT NULL,
    PRIMARY KEY (trade_id, trade_time)
);

SELECT create_hypertable('trades', 'trade_time', chunk_time_interval => INTERVAL '1 day');

CREATE INDEX ON trades (symbol, trade_time DESC);

CREATE TABLE ohlcv_1m (
    symbol       TEXT         NOT NULL,
    window_start TIMESTAMPTZ  NOT NULL,
    open         NUMERIC      NOT NULL,
    high         NUMERIC      NOT NULL,
    low          NUMERIC      NOT NULL,
    close        NUMERIC      NOT NULL,
    volume       NUMERIC      NOT NULL,
    trade_count  INTEGER      NOT NULL,
    PRIMARY KEY (symbol, window_start)
);

SELECT create_hypertable('ohlcv_1m', 'window_start', chunk_time_interval => INTERVAL '1 day');
