"""
drex.util.config — Central config loader using pydantic-settings.

All services should subclass Settings and add service-specific fields.
Shared infrastructure config (Kafka, gRPC, DB) lives here.

Usage
-----
.. code-block:: python

    from drex.util.config import Settings

    class MyServiceSettings(Settings):
        my_feature_flag: bool = False

    config = MyServiceSettings()
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Base settings — reads from environment variables and .env files."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ── Kafka ──────────────────────────────────────────────────────────────
    kafka_bootstrap_servers: str = Field(
        default="localhost:9092",
        description="Comma-separated list of Kafka broker addresses.",
    )
    kafka_consumer_group_id: str = Field(
        default="drex-default",
        description="Default consumer group ID. Override per service.",
    )

    # ── gRPC ───────────────────────────────────────────────────────────────
    grpc_host: str = Field(default="0.0.0.0", description="gRPC server bind host.")
    grpc_port: int = Field(default=50051, description="gRPC server port.")

    # ── Observability ──────────────────────────────────────────────────────
    log_level: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    service_name: str = Field(default="drex-service", description="Used in traces and logs.")
