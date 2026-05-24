from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = "localhost:29092"
    schema_registry_url: str = "http://localhost:8081"
    kafka_topic_trades: str = "btcusdt-trades"
    kafka_topic_dlq: str = "btcusdt-trades-dlq"
    binance_ws_url: str = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
