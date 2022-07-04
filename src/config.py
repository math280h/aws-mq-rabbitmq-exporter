from decouple import config

# Scrape Config
SCRAPE_INTERVAL = config("SCRAPE_INTERVAL", default=15, cast=int)

# AWS Config
AWS_REGION = config("AWS_REGION")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")

# Broker Config
BROKER_FILTER = config("BROKER_FILTER", default=None)
BROKER_FILTER_KEY = config("BROKER_FILTER_KEY", default="BrokerName")

# MQ Config
MQ_USER = config("MQ_USER")
MQ_PASSWORD = config("MQ_PASSWORD")
VERIFY_SSL = config("VERIFY_SSL", default=True, cast=bool)

# Logging Config
LOG_LEVEL = config("LOG_LEVEL", default=None)
LOG_FORMAT = config("LOG_FORMAT", default="%(levelname)s:%(asctime)s:%(message)s")

# SERVER
HTTP_PORT = config("HTTP_PORT", default=8000)
