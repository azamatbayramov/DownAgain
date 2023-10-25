from time import sleep
from aiogram import Bot
import asyncio
from src.config import BOT_TOKEN, CHANNEL_ID, IP, PING_INTERVAL_IN_SEC

from src.database.db import init_db
from src.database.models.ping_result import PingResult, PingResultDB
from src.database.models.internet_down import InternetDown, InternetDownDB

from datetime import datetime
from pythonping import ping

from messages import format_internet_down_message

bot = Bot(BOT_TOKEN)


async def main():
    await init_db()

    while True:
        # Ping
        ping_time = datetime.datetime.now()
        response_list = ping(IP)

        # Save ping result into DB
        ping_result = await PingResult.construct(IP, ping_time, response_list)

        await ping_result.insert()

        # Get info about current ping result and current internet down
        current_internet_down = await InternetDownDB.get_current_internet_down()
        current_ping_result = await PingResultDB.get_last_ping_result()

        # If internet was not down and current ping was not success
        if current_internet_down is None and not current_ping_result.success:
            # Create new internet down and insert it into DB
            internet_down = await InternetDown.construct(current_ping_result.id)

            await internet_down.insert()
        # If internet was down and current ping was success
        elif current_internet_down is not None and current_ping_result.success:
            # End current internet down
            await current_internet_down.end(current_ping_result.id)

            # Send message about internet down
            bot.send_message(CHANNEL_ID, format_internet_down_message(current_internet_down))

        sleep(PING_INTERVAL_IN_SEC)


if __name__ == "__main__":
    asyncio.run(main())
