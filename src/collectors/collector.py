import logging
from typing import List

from prometheus_client.metrics_core import GaugeMetricFamily

from src.models.broker import Broker
from src.models.queue import Queue


class Collector(object):
    """Base class for a collector with utility functions."""

    def __init__(self, brokers: List[Broker]) -> None:
        logging.debug("Initializing MQCollector")

        self.brokers = brokers

        self.default_labels = ["broker_id", "broker_name", "broker_region"]
        self.labels = []

    def define_gauge(self, *, metric: str, help_text: str) -> GaugeMetricFamily:
        """Defines a GaugeMetric."""
        return GaugeMetricFamily(metric, help_text, labels=self.labels)

    @staticmethod
    def gather_queue_data(broker: Broker) -> List[Queue]:
        """Gather data about queues in the broker."""
        queues = []

        logging.debug("Gathering queue data")
        for queue in broker.get_api().queue.list():
            try:
                queues.append(
                    Queue(name=queue["name"], broker_id=broker.id, data=queue)
                )
                logging.info(
                    "Found data for Queue: <%s> On broker: <%s>:<%s>",
                    queue.get("name"),
                    broker.name,
                    broker.id,
                )
            except Exception as e:
                logging.fatal("Error while gathering data: %s", str(e))
                exit(1)

        return queues
