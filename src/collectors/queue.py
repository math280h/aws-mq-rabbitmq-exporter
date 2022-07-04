from collections.abc import Generator
import logging

from prometheus_client.core import InfoMetricFamily

from src.collectors.collector import Collector
from src.helpers import get_length


class QueueCollector(Collector):
    """Collect data about queues in brokers."""

    def collect(self) -> Generator:
        """Collect data for Prometheus."""
        logging.debug("Defining metrics")

        self.labels = ["queue_name"] + self.default_labels

        # Memory
        memory_gauge = self.define_gauge(metric="queue_memory", help_text="Help text")

        # Message count
        message_ready_gauge = self.define_gauge(
            metric="queue_messages_ready", help_text="Help text"
        )
        message_total_gauge = self.define_gauge(
            metric="queue_messages_total", help_text="Help text"
        )
        messages_paged_out_gauge = self.define_gauge(
            metric="queue_messages_paged_out", help_text="Help text"
        )
        messages_persistent_gauge = self.define_gauge(
            metric="queue_messages_persistent", help_text="Help text"
        )
        messages_ram_gauge = self.define_gauge(
            metric="queue_messages_ram", help_text="Help text"
        )
        messages_ready_ram_gauge = self.define_gauge(
            metric="queue_messages_ready_ram", help_text="Help text"
        )
        messages_unacknowledged_gauge = self.define_gauge(
            metric="queue_messages_unacknowledged", help_text="Help text"
        )
        messages_unacknowledged_ram_gauge = self.define_gauge(
            metric="queue_messages_unacknowledged_ram", help_text="Help text"
        )

        # Message rates
        message_ready_rate_gauge = self.define_gauge(
            metric="queue_messages_ready_rate", help_text="Help text"
        )
        messages_unacknowledged_rate_gauge = self.define_gauge(
            metric="queue_messages_unacknowledged_rate", help_text="Help text"
        )

        # Message bytes
        message_bytes_gauge = self.define_gauge(
            metric="queue_message_bytes", help_text="Help text"
        )
        message_bytes_paged_out_gauge = self.define_gauge(
            metric="queue_message_bytes_paged_out", help_text="Help text"
        )
        message_bytes_persistent_gauge = self.define_gauge(
            metric="queue_message_bytes_persistent", help_text="Help text"
        )
        message_bytes_ram_gauge = self.define_gauge(
            metric="queue_message_bytes_ram", help_text="Help text"
        )
        message_bytes_ready_gauge = self.define_gauge(
            metric="queue_message_bytes_ready", help_text="Help text"
        )
        message_bytes_unacknowledged_gauge = self.define_gauge(
            metric="queue_message_bytes_unacknowledged", help_text="Help text"
        )

        # Message stats
        message_stats_publish_gauge = self.define_gauge(
            metric="queue_message_stats_publish", help_text="Help text"
        )
        message_stats_publish_rate_gauge = self.define_gauge(
            metric="queue_message_stats_publish_rate", help_text="Help text"
        )

        # Message details
        message_details_rate_gauge = self.define_gauge(
            metric="queue_message_details_rate", help_text="Help text"
        )

        # Consumer
        consumer_gauge = self.define_gauge(
            metric="queue_consumers", help_text="Help text"
        )
        consumer_cap_gauge = self.define_gauge(
            metric="queue_consumer_capacity", help_text="Help text"
        )
        consumer_util_gauge = self.define_gauge(
            metric="queue_consumer_utilisation", help_text="Help text"
        )

        # Secondary Nodes
        secondary_nodes_gauge = self.define_gauge(
            metric="queue_secondary_nodes_count", help_text="Help text"
        )
        secondary_nodes_synced_gauge = self.define_gauge(
            metric="queue_synchronised_nodes_count", help_text="Help text"
        )
        secondary_nodes_reco_gauge = self.define_gauge(
            metric="queue_recoverable_nodes_count", help_text="Help text"
        )

        # Reductions
        reduction_gauge = self.define_gauge(
            metric="queue_reductions", help_text="Help text"
        )
        reduction_rate_gauge = self.define_gauge(
            metric="queue_reductions_rate", help_text="Help text"
        )

        # Avg ingress/egress rate
        avg_ack_egress_gauge = self.define_gauge(
            metric="queue_avg_ack_egress_rate", help_text="Help text"
        )
        avg_ack_ingress_gauge = self.define_gauge(
            metric="queue_avg_ack_ingress_rate", help_text="Help text"
        )
        avg_egress_gauge = self.define_gauge(
            metric="queue_avg_egress_rate", help_text="Help text"
        )
        avg_ingress_gauge = self.define_gauge(
            metric="queue_avg_ingress_rate", help_text="Help text"
        )

        # Info
        queue_info = InfoMetricFamily("queue_info", "Help text", labels=self.labels)
        effective_policy_definition_info = InfoMetricFamily(
            "queue_effective_policy_definition", "Help text", labels=self.labels
        )

        logging.debug("Setting metric values")
        for broker in self.brokers:
            for queue in self.gather_queue_data(broker):
                labels = [queue.name, broker.id, broker.name, broker.region]

                # Memory
                memory_gauge.add_metric([queue.name], queue.zero_get("memory"))

                # Messages
                message_ready_gauge.add_metric(labels, queue.zero_get("messages_ready"))
                message_total_gauge.add_metric(labels, queue.zero_get("messages"))
                messages_paged_out_gauge.add_metric(
                    labels,
                    queue.zero_get("messages_paged_out"),
                )
                messages_persistent_gauge.add_metric(
                    labels,
                    queue.zero_get("messages_persistent"),
                )
                messages_ram_gauge.add_metric(labels, queue.zero_get("messages_ram"))
                messages_ready_ram_gauge.add_metric(
                    labels,
                    queue.zero_get("messages_ready_ram"),
                )
                messages_unacknowledged_gauge.add_metric(
                    labels,
                    queue.zero_get("messages_unacknowledged"),
                )
                messages_unacknowledged_ram_gauge.add_metric(
                    labels,
                    queue.zero_get("messages_unacknowledged_ram"),
                )

                # Message Rates
                message_ready_rate_gauge.add_metric(
                    labels,
                    queue.zero_get("rate", entrypoint="messages_ready_details"),
                )
                messages_unacknowledged_rate_gauge.add_metric(
                    labels,
                    queue.zero_get(
                        "rate", entrypoint="messages_unacknowledged_details"
                    ),
                )

                # Message bytes
                message_bytes_gauge.add_metric(labels, queue.zero_get("message_bytes"))
                message_bytes_paged_out_gauge.add_metric(
                    labels,
                    queue.zero_get("message_bytes_paged_out"),
                )
                message_bytes_persistent_gauge.add_metric(
                    labels,
                    queue.zero_get("message_bytes_persistent"),
                )
                message_bytes_ram_gauge.add_metric(
                    labels,
                    queue.zero_get("message_bytes_ram"),
                )
                message_bytes_ready_gauge.add_metric(
                    labels,
                    queue.zero_get("message_bytes_ready"),
                )
                message_bytes_unacknowledged_gauge.add_metric(
                    labels,
                    queue.zero_get("message_bytes_unacknowledged"),
                )

                # Message stats
                message_stats_publish_gauge.add_metric(
                    labels, queue.zero_get("publish", entrypoint="message_stats")
                )
                message_stats_publish_rate_gauge.add_metric(
                    labels,
                    queue.zero_get(
                        "rate",
                        entrypoint=queue.zero_get(
                            "publish_details",
                            entrypoint="message_stats",
                            return_type="dict",
                        ),
                    ),
                )

                # Message details
                message_details_rate_gauge.add_metric(
                    labels,
                    queue.zero_get("rate", entrypoint="messages_details"),
                )

                # Consumer
                consumer_gauge.add_metric(labels, queue.zero_get("consumers"))
                consumer_cap_gauge.add_metric(
                    labels,
                    queue.zero_get("consumer_capacity"),
                )
                consumer_util_gauge.add_metric(
                    labels,
                    queue.zero_get("consumer_utilisation"),
                )

                reduction_gauge.add_metric(labels, queue.zero_get("reductions"))
                reduction_rate_gauge.add_metric(
                    labels,
                    queue.zero_get("rate", entrypoint="reductions_details"),
                )

                secondary_nodes_gauge.add_metric(
                    labels,
                    get_length(queue.zero_get("slave_nodes", return_type="list")),
                )
                secondary_nodes_synced_gauge.add_metric(
                    labels,
                    get_length(
                        queue.zero_get("synchronised_slave_nodes", return_type="list")
                    ),
                )
                secondary_nodes_reco_gauge.add_metric(
                    labels,
                    get_length(
                        queue.zero_get("recoverable_slaves", return_type="list")
                    ),
                )

                avg_ack_egress_gauge.add_metric(
                    labels,
                    queue.zero_get(
                        "avg_ack_egress_rate", entrypoint="backing_queue_status"
                    ),
                )
                avg_ack_ingress_gauge.add_metric(
                    labels,
                    queue.zero_get(
                        "avg_ack_ingress_rate", entrypoint="backing_queue_status"
                    ),
                )
                avg_egress_gauge.add_metric(
                    labels,
                    queue.zero_get(
                        "avg_egress_rate", entrypoint="backing_queue_status"
                    ),
                )
                avg_ingress_gauge.add_metric(
                    labels,
                    queue.zero_get(
                        "avg_ingress_rate", entrypoint="backing_queue_status"
                    ),
                )

                effective_policy_definition_info.add_metric(
                    labels,
                    {
                        "ha_mode": queue.zero_get(
                            "ha_mode",
                            entrypoint="effective_policy_definition",
                            return_type="str",
                        ),
                        "ha_sync_mode": queue.zero_get(
                            "ha-sync-mode",
                            entrypoint="effective_policy_definition",
                            return_type="str",
                        ),
                        "max_length": queue.zero_get(
                            "max-length",
                            entrypoint="effective_policy_definition",
                            return_type="str",
                        ),
                        "overflow": queue.zero_get(
                            "overflow",
                            entrypoint="effective_policy_definition",
                            return_type="str",
                        ),
                        "queue_mode": queue.zero_get(
                            "queue-mode",
                            entrypoint="effective_policy_definition",
                            return_type="str",
                        ),
                    },
                )

                # Info
                info = {
                    "primary_node": queue.zero_get("node", return_type="str"),
                    "policy": queue.zero_get("policy", return_type="str"),
                    "durable": queue.zero_get("durable", return_type="str"),
                    "state": queue.zero_get("state", return_type="str"),
                    "vhost": queue.zero_get("vhost", return_type="str"),
                    "type": queue.zero_get("type", return_type="str"),
                    "auto_delete": queue.zero_get("auto_delete", return_type="str"),
                    "single_active_consumer_tag": queue.zero_get(
                        "single_active_consumer_tag", return_type="str"
                    ),
                    "exclusive_consumer_tag": queue.zero_get(
                        "exclusive_consumer_tag", return_type="str"
                    ),
                    "exclusive": queue.zero_get("exclusive", return_type="str"),
                }

                if "arguments" in queue.data:
                    for key, value in queue.data["arguments"].items():
                        if key in info.keys():
                            logging.error(
                                "A queue argument name duplicates static information key: %s - Skipping argument",
                                key,
                            )
                            continue
                        info[key.replace("-", "_")] = str(value)
                else:
                    logging.debug("No arguments found for queue, skipping step")

                queue_info.add_metric(labels, info)

        logging.debug("Returning metrics")

        yield message_ready_gauge
        yield message_total_gauge
        yield messages_paged_out_gauge
        yield messages_persistent_gauge
        yield messages_ram_gauge
        yield messages_ready_ram_gauge
        yield messages_unacknowledged_gauge
        yield messages_unacknowledged_ram_gauge

        yield message_ready_rate_gauge
        yield messages_unacknowledged_rate_gauge

        yield message_bytes_gauge
        yield message_bytes_paged_out_gauge
        yield message_bytes_persistent_gauge
        yield message_bytes_ram_gauge
        yield message_bytes_ready_gauge
        yield message_bytes_unacknowledged_gauge

        yield message_stats_publish_gauge
        yield message_stats_publish_rate_gauge

        yield message_details_rate_gauge

        yield consumer_gauge
        yield consumer_cap_gauge
        yield consumer_util_gauge

        yield reduction_gauge
        yield reduction_rate_gauge

        yield secondary_nodes_gauge
        yield secondary_nodes_synced_gauge
        yield secondary_nodes_reco_gauge

        yield avg_ack_egress_gauge
        yield avg_ack_ingress_gauge
        yield avg_egress_gauge
        yield avg_ingress_gauge

        yield effective_policy_definition_info
        yield queue_info
