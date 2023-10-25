from time import sleep
from aiogram import Bot
import asyncio
from src.config import BOT_TOKEN, CHANNEL_ID

from src.database.db import init_db
from src.database.models.ping_result import PingResultDB

from src.ping import ping_and_save

IP = "8.8.8.8"
INTERVAL = 30

bot = Bot(BOT_TOKEN)


async def main():
    await init_db()

    while True:
        await ping_and_save()

        ping_result = await PingResultDB.get_last_ping_result()

        await bot.send_message(CHANNEL_ID, str(ping_result))

        sleep(INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
