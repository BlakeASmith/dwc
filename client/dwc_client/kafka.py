import json
from typing import Callable, Iterable, Any
import kafka.errors
from kafka import KafkaProducer, KafkaConsumer
from functools import partial
from dataclasses import asdict, is_dataclass


def json_serializer(value: dict) -> str:
    return json.dumps(value).encode("utf-8")


def dataclass_serializer(dc) -> str:
    return json_serializer(asdict(dc))


def produce_to_topic(
    iterable: Iterable[Any], 
    topic: str, 
    bootstraps: Iterable[str],
    serializer: Callable[[Any], str] = dataclass_serializer,
):
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstraps,
            value_serializer=serializer,
        )
    except kafka.errors.NoBrokersAvailable:
        raise ValueError("Invalid bootstrap servers.")

    for value in iterable:
        yield producer.send(topic, value)

def produce(
    topic: str,
    bootstraps: Iterable[str],
):
    return partial(produce_to_topic, topic=topic, bootstraps=bootstraps)


def consume(
    topic: str,
    bootstraps: Iterable[str],
    deserializer: Callable[[str], Any],
):
    return KafkaConsumer(topic, bootstrap_servers=bootstraps, value_deserializer=deserializer)