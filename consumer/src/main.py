import logging

from src.config import settings
from src.kafka.consumer import build_consumer, build_avro_deserializer, deserialize
from src.transform.ohlcv import OhlcvAccumulator
from src.db.writer import build_connection, write_candles

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting Sentry OHLCV consumer")
    consumer = build_consumer()
    deserializer = build_avro_deserializer()
    conn = build_connection()
    accumulator = OhlcvAccumulator()

    consumer.subscribe([settings.kafka_topic_trades])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error("Consumer error: %s", msg.error())
                continue

            record = deserialize(deserializer, msg)
            completed, active = accumulator.update(record)

            if completed:
                logger.info("Flushing %d completed candle(s)", len(completed))
            write_candles(conn, completed + [active])
    finally:
        consumer.close()
        conn.close()


if __name__ == "__main__":
    main()
