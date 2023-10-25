from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.database.models.ping_result import PingResult
from src.database.models.internet_down import InternetDown

from src.config import MONGO_URL


async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client.DownAgain,
        document_models=[PingResult, InternetDown]
    )
