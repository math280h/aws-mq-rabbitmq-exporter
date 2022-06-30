from dataclasses import dataclass

from amqpstorm import management

from src.config import MQ_USER, MQ_PASSWORD, VERIFY_SSL


@dataclass
class Broker:
    id: str
    name: str
    region: str

    def get_url(self):
        return f"https://{self.id}.mq.{self.region}.amazonaws.com:15671"

    def get_api(self) -> management.ManagementApi:
        return management.ManagementApi(
            self.get_url(),
            MQ_USER,
            MQ_PASSWORD,
            verify=VERIFY_SSL,
        )
