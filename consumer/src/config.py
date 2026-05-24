from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = "localhost:29092"
    schema_registry_url: str = "http://localhost:8081"
    kafka_topic_trades: str = "btcusdt-trades"
    kafka_consumer_group: str = "sentry-ohlcv-consumer"
    timescaledb_host: str = "localhost"
    timescaledb_port: int = 5432
    timescaledb_user: str = "sentry"
    timescaledb_password: str = "sentry"
    timescaledb_db: str = "sentry"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
