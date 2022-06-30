import logging
from dataclasses import dataclass

from amqpstorm import management

from src.config import MQ_USER, MQ_PASSWORD, VERIFY_SSL


@dataclass
class Queue:
    name: str
    broker_id: str
    data: any

    def entrypoint(self, key):
        if type(key) is dict:
            return key

        val = self.data.get(key)

        if val is None:
            return {}
        else:
            return self.data[key]

    def zero_get(self, key: str, entrypoint=None, return_type="int"):
        if entrypoint is not None:
            entrypoint_data = self.entrypoint(entrypoint)
            data = entrypoint_data.get(key)
        else:
            data = self.data.get(key)

        text = None
        return_val = None
        if return_type == "int":
            text = "int(0)"
            return_val = 0
        elif return_type == "str":
            text = "str(None)"
            return_val = str(None)
        elif return_type == "list":
            text = "List[]"
            return_val = []
        elif return_type == "dict":
            text = "dict"
            return_val = {}
        else:
            logging.fatal("Invalid return type")
            exit(2)

        if data is None:
            logging.warning(
                f"Unable to find data for: {self.name}:{key} - Defaulting to {text}"
            )

            return return_val
        else:
            if return_type == "int":
                return int(data)
            elif return_type == "str":
                return str(data)
            else:
                return
