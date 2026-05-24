import asyncio
import json
import logging

import websockets
from confluent_kafka import Producer
from confluent_kafka.schema_registry.avro import AvroSerializer

from src.config import settings
from src.kafka.producer import produce_trade, flush
from src.transform.mapper import map_binance_trade

logger = logging.getLogger(__name__)

_INITIAL_BACKOFF = 1
_MAX_BACKOFF = 60


async def stream(producer: Producer, serializer: AvroSerializer) -> None:
    backoff = _INITIAL_BACKOFF

    while True:
        try:
            async with websockets.connect(settings.binance_ws_url) as ws:
                logger.info("Connected to Binance WebSocket")
                backoff = _INITIAL_BACKOFF

                async for raw in ws:
                    payload = json.loads(raw)
                    record = map_binance_trade(payload)
                    produce_trade(producer, serializer, record)

        except websockets.ConnectionClosed as e:
            logger.warning("Connection closed: %s. Reconnecting in %ss", e, backoff)
        except Exception as e:
            logger.error("Unexpected error: %s. Reconnecting in %ss", e, backoff)
        finally:
            flush(producer)

        await asyncio.sleep(backoff)
        backoff = min(backoff * 2, _MAX_BACKOFF)
