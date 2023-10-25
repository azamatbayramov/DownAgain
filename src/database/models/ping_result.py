from beanie import Document

from datetime import datetime
from pytz import timezone

from src.config import TIMEZONE

from pythonping.executor import ResponseList


class PingResult(Document):
    id: int

    ip: str
    datetime_utc: datetime

    success: bool

    rtt_min_ms: float
    rtt_avg_ms: float
    rtt_max_ms: float

    packet_loss: float

    @staticmethod
    async def construct(ip: str, datetime: datetime, response_list: ResponseList):
        ping_result = PingResult(
            id=await PingResult.count() + 1,
            ip=ip,
            datetime_utc=datetime,
            success=response_list.success(),
            rtt_min_ms=response_list.rtt_min_ms,
            rtt_avg_ms=response_list.rtt_avg_ms,
            rtt_max_ms=response_list.rtt_max_ms,
            packet_loss=response_list.packet_loss
        )

        return ping_result

    @property
    def datetime(self) -> datetime:
        return self.datetime_utc.astimezone(timezone(TIMEZONE))

    def __str__(self) -> str:
        return f"Ping result #{self.id}:\n{self.ip}, {self.datetime}\n" \
               f"RTT min/avg/max: {self.rtt_min_ms}/{self.rtt_avg_ms}/{self.rtt_max_ms}\n" \
               f"Success: {self.success}, packet loss: {self.packet_loss}"

    class Settings:
        name = "ping_results"


class PingResultDB:
    @staticmethod
    async def get_last_ping_result() -> PingResult:
        return await PingResult.find_one({"_id": await PingResult.count()})

    @staticmethod
    async def get_all_ping_results() -> list[PingResult]:
        return await PingResult.find_all()
