from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.database.models.ping_result import PingResult

from src.config import MONGO_URL


async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client.FellAgain,
        document_models=[PingResult]
    )
