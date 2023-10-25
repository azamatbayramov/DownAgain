from beanie import Document

from datetime import datetime

from pythonping.executor import ResponseList


class PingResult(Document):
    id: int

    ip: str
    datetime: datetime

    success: bool

    rtt_min_ms: float
    rtt_avg_ms: float
    rtt_max_ms: float

    packet_loss: float

    def fill(self, ip: str, datetime: datetime, response_list: ResponseList):
        self.id = PingResult.count() + 1

        self.ip = ip
        self.datetime = datetime

        self.success = response_list.success()

        self.rtt_min_ms = response_list.rtt_min_ms
        self.rtt_avg_ms = response_list.rtt_avg_ms
        self.rtt_max_ms = response_list.rtt_max_ms

        self.packet_loss = response_list.packet_loss

        return self

    class Settings:
        name = "ping_results"