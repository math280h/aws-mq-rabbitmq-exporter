from decouple import config

# Scrape Config
SCRAPE_INTERVAL = config("SCRAPE_INTERVAL", default=15)

# AWS Config
AWS_REGION = config("AWS_REGION")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")

# Broker Config
BROKER_FILTER = config("BROKER_FILTER", default=None)

# MQ Config
MQ_USER = config("MQ_USER")
MQ_PASSWORD = config("MQ_PASSWORD")
VERIFY_SSL = config("VERIFY_SSL", default=True, cast=bool)

# Debug
LOG_LEVEL = config("LOG_LEVEL", default=None)
