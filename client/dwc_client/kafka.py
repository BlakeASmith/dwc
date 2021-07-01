import json
from typing import Iterable, Tuple
import kafka.errors
from kafka import KafkaProducer
from functools import partial


def json_serializer(value: dict) -> str:
    return json.dumps(value).encode("utf-8")


def produce_to_topic(iterable: Iterable[Tuple[str, dict]], topic: str, bootstraps: Iterable[str]):
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstraps,
            value_serializer=json_serializer,
        )
    except kafka.errors.NoBrokersAvailable:
        raise ValueError("Invalid bootstrap servers.")

    for key, value in iterable:
        yield producer.send(key, value)

def produce(
    topic: str,
    bootstraps: Iterable[str],
):
    return partial(produce_to_topic, topic=topic, bootstraps=bootstraps)