from pythonping import ping
from time import sleep
from aiogram import Bot
import asyncio
from src.config import BOT_TOKEN, CHANNEL_ID


IP = "8.8.8.8"
INTERVAL = 30

bot = Bot(BOT_TOKEN)

async def main():
    while True:
        response_list = ping(IP, verbose=True)

        if not response_list.success():
            await bot.send_message(CHANNEL_ID, "Oh, no, Internet Fell Again")

        sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
