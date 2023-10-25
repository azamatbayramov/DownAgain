import os
from tzlocal import get_localzone_name

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

IP = "8.8.8.8"
PING_INTERVAL_IN_SEC = 10

MONGO_URL = "mongodb://mongodb:27017"

TIMEZONE_NAME = get_localzone_name()
