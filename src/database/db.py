from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from pythonping.executor import ResponseList

from datetime import datetime

from src.database.models.ping_result import PingResult

from src.config import MONGO_URL


async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client.FellAgain,
        document_models=[PingResult]
    )


async def save_ping_info_into_db(ip: str, ping_time: datetime, response_list: ResponseList):
    ping_result = PingResult(
        ip=ip,
        datetime=ping_time,

        success=response_list.success(),

        rtt_min_ms=response_list.rtt_min_ms,
        rtt_avg_ms=response_list.rtt_avg_ms,
        rtt_max_ms=response_list.rtt_max_ms,

        packet_loss=response_list.packet_loss
    )

    await ping_result.insert()
