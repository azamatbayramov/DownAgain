from beanie import Document
from datetime import datetime, timedelta

from src.database.models.ping_result import PingResult


class InternetDown(Document):
    id: int

    is_ended: bool = False

    start_ping_result_id: int
    end_ping_result_id: int | None = None

    @staticmethod
    async def construct(start_ping_result_id: int):
        internet_down = InternetDown(
            id=await InternetDown.count() + 1,
            start_ping_result_id=start_ping_result_id
        )

        return internet_down

    async def end(self, end_ping_result_id: int):
        self.is_ended = True
        self.end_ping_result_id = end_ping_result_id

        await self.save()

    async def get_start_ping_result(self) -> PingResult:
        return await PingResult.find_one({"_id": self.start_ping_result_id})

    async def get_end_ping_result(self) -> PingResult | None:
        if self.end_ping_result_id is None:
            return None

        return await PingResult.find_one({"_id": self.end_ping_result_id})

    async def get_start_datetime(self) -> datetime:
        return (await self.get_start_ping_result()).datetime

    async def get_end_datetime(self) -> datetime | None:
        if self.end_ping_result_id is None:
            return None

        return (await self.get_end_ping_result()).datetime

    async def get_duration(self) -> timedelta | None:
        if not self.is_ended:
            return None

        return (await self.get_end_datetime()) - (await self.get_start_datetime())

    def __str__(self) -> str:
        return f"InternetDown #{self.id}\n"\
               f"Is ended: {self.is_ended}\n"\
               f"Start ping result id: {self.start_ping_result_id}\n"\
               f"End ping result id: {self.end_ping_result_id}"

    class Settings:
        name = "internet_downs"


class InternetDownDB:
    @staticmethod
    async def get_current_internet_down() -> InternetDown:
        return await InternetDown.find_one({"is_ended": False})

    @staticmethod
    async def get_last_internet_down() -> InternetDown:
        return await InternetDown.find_one({"_id": await InternetDown.count()})

    @staticmethod
    async def get_all_internet_downs() -> list[InternetDown]:
        return await InternetDown.find_all()
