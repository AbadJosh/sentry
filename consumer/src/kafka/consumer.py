from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

from src.config import settings


def build_consumer() -> Consumer:
    return Consumer({
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "group.id": settings.kafka_consumer_group,
        "auto.offset.reset": "earliest",
    })


def build_avro_deserializer() -> AvroDeserializer:
    registry_client = SchemaRegistryClient({"url": settings.schema_registry_url})
    return AvroDeserializer(registry_client)


def deserialize(deserializer: AvroDeserializer, message) -> dict:
    return deserializer(message.value(), SerializationContext(message.topic(), MessageField.VALUE))
