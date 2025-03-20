from faststream.asgi import AsgiFastStream
from faststream.kafka import KafkaBroker

from src.settings import app_settings


def add_broker(application: AsgiFastStream) -> None:
    broker = KafkaBroker(app_settings.KAFKA_BOOTSTRAP_SERVERS)
    application.set_broker(broker)
