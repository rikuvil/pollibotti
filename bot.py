import os
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = Bot(token=BOT_TOKEN)

FI_WEEKDAYS = [
    "Maanantai",
    "Tiistai",
    "Keskiviikko",
    "Torstai",
    "Perjantai",
    "Lauantai",
    "Sunnuntai"
]

async def send_weekly_poll():
    helsinki_tz = ZoneInfo("Europe/Helsinki")
    now = datetime.now(helsinki_tz)

    next_week_target = now + timedelta(days=7)
    week_number = next_week_target.isocalendar()[1]

    next_monday = next_week_target - timedelta(days=next_week_target.weekday())

    options = []
    for i in range(7):
        day = next_monday + timedelta(days=i)
        date_str = day.strftime("%d.%m")
        options.append(f"{FI_WEEKDAYS[i]} {date_str}")

    options.extend([
        "Koko viikko / joustava",
        "En tiedä vielä 🤷",
        "En pääse 🙁",
        "Kuhan vastauksia kattelen 🕵️"
    ])

    async with bot:
        await bot.send_poll(
            chat_id=CHAT_ID,
            question=f"🎲 Viikon {week_number} pelipäivät?",
            options=options,
            is_anonymous=False,
            allows_multiple_answers=True
        )

    print(
        f"Poll for week {week_number} sent at "
        f"{datetime.now(helsinki_tz)}"
    )

if __name__ == "__main__":
    asyncio.run(send_weekly_poll())

# Pyörii cronin kautta kerran viikossa sunnuntaina klo 12:00