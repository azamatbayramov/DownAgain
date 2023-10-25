from beanie import Document


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
