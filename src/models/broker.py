from dataclasses import dataclass
import logging

from amqpstorm import management

from src.config import MQ_PASSWORD, MQ_USER, VERIFY_SSL


@dataclass
class Broker:
    """Dataclass for a Broker."""

    id: str
    name: str
    region: str

    def get_url(self) -> str:
        """Get management url for broker."""
        return f"https://{self.id}.mq.{self.region}.amazonaws.com:15671"

    def get_api(self) -> management.ManagementApi:
        """Get API Client for broker."""
        try:
            return management.ManagementApi(
                self.get_url(),
                MQ_USER,
                MQ_PASSWORD,
                verify=VERIFY_SSL,
            )
        except Exception as e:
            logging.fatal("Unable to establish API Connection")
            logging.fatal(e)
            exit(1)
