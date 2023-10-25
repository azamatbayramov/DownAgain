from beanie import Document

from datetime import datetime


class PingResult(Document):
    ip: str
    datetime: datetime

    rtt_min_ms: float
    rtt_avg_ms: float
    rtt_max_ms: float

    packet_loss: float

    class Settings:
        name = "ping_results"
