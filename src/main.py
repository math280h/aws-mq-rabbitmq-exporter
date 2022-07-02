import logging
import re
import time

import boto3
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from src.collectors.queue import QueueCollector
from src.config import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
    BROKER_FILTER,
    BROKER_FILTER_KEY,
    HTTP_PORT,
    LOG_FORMAT,
    LOG_LEVEL,
    SCRAPE_INTERVAL,
)
from src.models.broker import Broker


def start() -> None:
    """Boostrap application."""
    log_level = logging.WARNING
    if LOG_LEVEL is not None:
        if LOG_LEVEL.lower() == "debug":
            log_level = logging.DEBUG
        elif LOG_LEVEL.lower() == "error":
            log_level = logging.ERROR
        elif LOG_LEVEL.lower() == "critical":
            log_level = logging.CRITICAL
        else:
            log_level = logging.INFO

    logging.basicConfig(
        format=LOG_FORMAT,
        encoding="utf-8",
        level=log_level,
    )

    client = boto3.client(
        "mq",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    response = client.list_brokers(MaxResults=100)

    broker_filter = re.compile(BROKER_FILTER)

    brokers = []

    for broker in response["BrokerSummaries"]:
        if broker_filter.match(broker[BROKER_FILTER_KEY]) is not None:
            print(broker)
            brokers.append(
                Broker(
                    name=broker["BrokerName"],
                    id=broker["BrokerId"],
                    region=broker["BrokerArn"].split(":")[3],
                )
            )

    if not brokers:
        logging.fatal("No brokers discovered.")
        exit(1)

    REGISTRY.register(QueueCollector(brokers))

    start_http_server(HTTP_PORT)

    while True:
        logging.debug("Waiting for timeout")
        time.sleep(SCRAPE_INTERVAL)


if __name__ == "__main__":
    start()
