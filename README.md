# aws-mq-rabbitmq-exporter

Prometheus exporter specifically built for AWS MQ RabbitMQ
with support for broker auto-discovery.

## Note

This exporter is currently in early development and may introduce breaking features

## Deployment

### Terraform

<details>
  <summary>Click to expand!</summary>

````terraform
resource "kubernetes_manifest" "deployment" {
    provider = kubernetes

    manifest = {
        apiVersion = "apps/v1"
        kind       = "Deployment"

        metadata = {
            namespace = "monitoring"
            name      = "mq-exporter"

            labels = {
                app = "mq-exporter"
            }
        }

        spec = {
            replicas = 1

            selector = {
                matchLabels = {
                    app = "mq-exporter"
                }
            }

            template = {
                metadata = {
                    name = "mq-exporter"

                    labels = {
                        app = "mq-exporter"
                    }
                }

                spec = {
                    terminationGracePeriodSeconds = 0

                    nodeSelector = {
                        role = "monitoring"
                    }

                    containers = [
                        {
                            name  = "mq-exporter"
                            image = "ghcr.io/math280h/aws-mq-rabbitmq-exporter:latest"

                            env = [
                                {
                                    name  = "AWS_REGION"
                                    value = "us-east-1"
                                },
                                {
                                    name  = "AWS_ACCESS_KEY_ID"
                                    value = var.AWS_ACCESS_KEY_ID
                                },
                                {
                                    name  = "AWS_SECRET_ACCESS_KEY"
                                    value = var.AWS_SECRET_ACCESS_KEY
                                },
                                {
                                    name  = "MQ_USER"
                                    value = var.MQ_USER
                                },
                                {
                                    name  = "MQ_PASSWORD"
                                    value = var.MQ_PASSWORD
                                },
                                {
                                    name = "SCRAPE_INTERVAL"
                                    value = 30
                                },
                                {
                                    name  = "PYTHONUNBUFFERED"
                                    value = 1
                                }
                            ]

                            resources = {
                                requests = {
                                    cpu    = "500m"
                                    memory = "1Gi"
                                }
                                limits = {
                                    cpu    = "2"
                                    memory = "2Gi"
                                }
                            }
                        }
                    ]
                }
            }
        }
    }
}

resource "kubernetes_service" "service" {
    provider = kubernetes

    metadata {
        name      = "mq-exporter"
        namespace = "monitoring"

        labels = {
            app = "mq-exporter"
        }
    }

    spec {
        selector = {
            app = "mq-exporter"
        }

        port {
            port        = 8080
            target_port = 8000
            protocol    = "TCP"
        }
    }
}
````
</details>

