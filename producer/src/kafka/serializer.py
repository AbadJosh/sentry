from importlib.resources import files

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField

from src.config import settings


def _load_schema() -> str:
    return files("src.schemas").joinpath("btc_trade.avsc").read_text()


def build_avro_serializer() -> AvroSerializer:
    registry_client = SchemaRegistryClient({"url": settings.schema_registry_url})
    return AvroSerializer(registry_client, _load_schema())


def serialize(serializer: AvroSerializer, record: dict) -> bytes:
    return serializer(record, SerializationContext(settings.kafka_topic_trades, MessageField.VALUE))
