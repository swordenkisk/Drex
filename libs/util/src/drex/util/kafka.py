"""
drex.util.kafka — Thin wrappers around confluent-kafka for producing and
consuming Drex domain events.

Rules
-----
- Events are immutable; never republish a modified event.
- Schemas are validated before publishing using drex.schema types.
- Consumers must be driven by Kafka (no in-process projection handlers).
- Event names must use PascalCase.

Usage — Producer
----------------
.. code-block:: python

    from drex.util.kafka import KafkaProducer
    from my_service.events import OrderPlaced

    producer = KafkaProducer(bootstrap_servers="localhost:9092")
    event = OrderPlaced(order_id=uuid4(), total_amount=99.99)
    producer.publish("orders", event)
    producer.flush()

Usage — Consumer
----------------
.. code-block:: python

    from drex.util.kafka import KafkaConsumer

    consumer = KafkaConsumer(
        topics=["orders"],
        group_id="inventory-service",
        bootstrap_servers="localhost:9092",
    )
    for message in consumer.stream():
        print(message.value())
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from typing import TYPE_CHECKING

from confluent_kafka import Consumer, KafkaError, KafkaException, Producer
from confluent_kafka import Message as KafkaMessage

if TYPE_CHECKING:
    from drex.schema.events import BaseEvent

logger = logging.getLogger(__name__)


class KafkaProducer:
    """Wraps confluent Producer with typed event publishing."""

    def __init__(self, bootstrap_servers: str = "localhost:9092", **extra_config: object) -> None:
        self._producer = Producer(
            {"bootstrap.servers": bootstrap_servers, **extra_config}
        )

    def publish(self, topic: str, event: "BaseEvent") -> None:
        """Serialize *event* and produce it to *topic*."""
        payload = event.to_kafka_value()
        self._producer.produce(
            topic=topic,
            value=payload,
            key=str(event.event_id).encode("utf-8"),
            on_delivery=self._delivery_report,
        )

    def flush(self, timeout: float = 10.0) -> None:
        self._producer.flush(timeout=timeout)

    @staticmethod
    def _delivery_report(err: KafkaError | None, msg: KafkaMessage) -> None:
        if err:
            logger.error("Kafka delivery failed: %s", err)
        else:
            logger.debug("Delivered to %s [%d] @ %d", msg.topic(), msg.partition(), msg.offset())


class KafkaConsumer:
    """Wraps confluent Consumer with a simple streaming iterator."""

    def __init__(
        self,
        topics: list[str],
        group_id: str,
        bootstrap_servers: str = "localhost:9092",
        auto_offset_reset: str = "earliest",
        **extra_config: object,
    ) -> None:
        self._consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_servers,
                "group.id": group_id,
                "auto.offset.reset": auto_offset_reset,
                "enable.auto.commit": True,
                **extra_config,
            }
        )
        self._consumer.subscribe(topics)

    def stream(self, timeout: float = 1.0) -> Iterator[KafkaMessage]:
        """Yield messages indefinitely. Exits cleanly on KeyboardInterrupt."""
        try:
            while True:
                msg = self._consumer.poll(timeout=timeout)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    raise KafkaException(msg.error())
                yield msg
        except KeyboardInterrupt:
            logger.info("Consumer loop interrupted.")
        finally:
            self._consumer.close()
