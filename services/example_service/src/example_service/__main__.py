"""
example_service.__main__ — Entry point.

Run with:
    python -m example_service
    # or via poetry script:
    example-service
"""

import logging
import signal
import sys

from drex.util.config import Settings
from drex.util.kafka import KafkaConsumer


def main() -> None:
    config = Settings()

    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    )
    logger = logging.getLogger("example_service")
    logger.info("Starting %s", config.service_name)

    consumer = KafkaConsumer(
        topics=["example-events"],
        group_id="example-service",
        bootstrap_servers=config.kafka_bootstrap_servers,
    )

    def _shutdown(sig: int, _frame: object) -> None:
        logger.info("Received signal %d — shutting down.", sig)
        sys.exit(0)

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    logger.info("Consuming from 'example-events'…")
    for msg in consumer.stream():
        logger.info("Received message: %s", msg.value())


if __name__ == "__main__":
    main()
