from time import sleep
from aiogram import Bot
import asyncio
from src.config import BOT_TOKEN, CHANNEL_ID, IP, PING_INTERVAL_IN_SEC

from src.database.db import init_db
from src.database.models.ping_result import PingResult, PingResultDB
from src.database.models.internet_down import InternetDown, InternetDownDB

from datetime import datetime
import pytz

from pythonping import ping

import logging

from src.messages import format_internet_down_message

bot = Bot(BOT_TOKEN)

logging.basicConfig(level=logging.INFO)


async def main():
    logging.info("Initializing database connection...")
    await init_db()

    while True:
        logging.info("----------------------------------")
        # Ping
        logging.info(f"Pinging {IP}...")
        ping_time = datetime.now(tz=pytz.timezone('Europe/Moscow'))
        response_list = ping(IP, verbose=True)

        # Save ping result into DB
        logging.info("Saving ping result into DB...")
        ping_result = await PingResult.construct(IP, ping_time, response_list)

        await ping_result.insert()

        # Get info about current ping result and current internet down
        logging.info("Getting info about current ping result and current internet down...")
        current_internet_down = await InternetDownDB.get_current_internet_down()
        current_ping_result = await PingResultDB.get_last_ping_result()

        logging.info(f"Current internet down:\n{current_internet_down}")
        logging.info(f"Current ping result:\n{current_ping_result}")

        # If internet was not down and current ping was not success
        if current_internet_down is None and not current_ping_result.success:
            logging.info("Internet is down!")

            # Create new internet down and insert it into DB
            logging.info("Creating new internet down and inserting it into DB...")
            internet_down = await InternetDown.construct(current_ping_result.id)

            await internet_down.insert()
        # If internet was down and current ping was success
        elif current_internet_down is not None and current_ping_result.success:
            logging.info("Internet is up!")

            # End current internet down
            logging.info("Ending current internet down...")
            await current_internet_down.end(current_ping_result.id)

            # Send message about internet down
            logging.info("Sending message about internet down...")
            await bot.send_message(
                CHANNEL_ID,
                await format_internet_down_message(current_internet_down)
            )

        logging.info(f"Sleeping for {PING_INTERVAL_IN_SEC} seconds...")
        sleep(PING_INTERVAL_IN_SEC)


if __name__ == "__main__":
    asyncio.run(main())
