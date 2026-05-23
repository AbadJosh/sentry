import json
import logging

from confluent_kafka import Producer
from confluent_kafka.schema_registry.avro import AvroSerializer

from src.config import settings
from src.kafka.serializer import serialize

logger = logging.getLogger(__name__)


def build_producer() -> Producer:
    return Producer({"bootstrap.servers": settings.kafka_bootstrap_servers})


def produce_trade(producer: Producer, serializer: AvroSerializer, record: dict) -> None:
    try:
        payload = serialize(serializer, record)
        producer.produce(topic=settings.kafka_topic_trades, value=payload)
    except Exception as e:
        logger.error("Failed to serialize record, routing to DLQ: %s", e)
        producer.produce(
            topic=settings.kafka_topic_dlq,
            value=json.dumps(record).encode("utf-8"),
        )


def flush(producer: Producer) -> None:
    producer.flush()
