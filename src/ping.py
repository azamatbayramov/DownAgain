import datetime
from pythonping import ping

from src.database.models.ping_result import PingResult

from src.config import IP


async def ping_and_save():
    ping_time = datetime.datetime.now()
    response_list = ping(IP)

    ping_result = await PingResult.construct(IP, ping_time, response_list)

    await ping_result.insert()
