from src.database.models.internet_down import InternetDown

from datetime import timedelta


def format_duration(duration: timedelta) -> str:
    seconds = duration.total_seconds()

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    return f"{hours}h {minutes}m {seconds}s"


async def format_internet_down_message(internet_down: InternetDown) -> str:
    start_datetime = (await internet_down.get_start_datetime()).strftime("%d.%m.%Y %H:%M:%S")
    end_datetime = (await internet_down.get_end_datetime()).strftime("%d.%m.%Y %H:%M:%S")

    duration = format_duration(await internet_down.get_duration())

    return f"Internet was down again!\n"\
           f"From {start_datetime} to {end_datetime}!.\n"\
           f"Duration: {duration}."
