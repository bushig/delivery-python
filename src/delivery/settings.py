from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    host: str = "localhost"
    port: int = 5432
    name: str = "delivery"
    user: str = "username"
    password: str = "secret"
    sslmode: str = "disable"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}?ssl={self.sslmode}"


class KafkaSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="KAFKA_")

    host: str = "localhost:9092"
    consumer_group: str = "delivery-group"
    basket_events_topic: str = "basket.events"
    order_events_topic: str = "order.events"


class GeoGrpcSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GEO_SERVICE_GRPC_")

    host: str = "0.0.0.0"
    port: int = 5004

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")

    http_port: int = 8082
    db: DatabaseSettings = DatabaseSettings()
    kafka: KafkaSettings = KafkaSettings()
    geo_grpc: GeoGrpcSettings = GeoGrpcSettings()


settings = AppSettings()
