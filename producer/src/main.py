import asyncio
import logging

from src.kafka.producer import build_producer
from src.kafka.serializer import build_avro_serializer
from src.client.binance import stream

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)

logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Starting Sentry producer")
    producer = build_producer()
    serializer = build_avro_serializer()
    await stream(producer, serializer)


if __name__ == "__main__":
    asyncio.run(main())
