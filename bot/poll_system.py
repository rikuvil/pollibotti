import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = Bot(token=BOT_TOKEN)

FI_WEEKDAYS = [
    "Ma | Mon",
    "Ti | Tue",
    "Ke | Wed",
    "To | Thu",
    "Pe | Fri",
    "La | Sat",
    "Su | Sun"
]


async def send_weekly_poll():
    helsinki_tz = ZoneInfo("Europe/Helsinki")
    now = datetime.now(helsinki_tz)

    close_date = now + timedelta(days=7)

    next_week = now + timedelta(days=7)
    week_number = next_week.isocalendar()[1]

    next_monday = next_week - timedelta(days=next_week.weekday())

    options = []
    for i in range(7):
        day = next_monday + timedelta(days=i)
        date_str = day.strftime("%d.%m")
        options.append(f"{FI_WEEKDAYS[i]} {date_str}")

    options.extend([
        "Koko viikko / joustava | Whole week / flexible",
        "En tiedä vielä 🤷 | I don't know yet",
        "En pääse 🙁 | Unable to make it",
        "Vastauksia katselen 🕵️ | Checking answers"
    ])

    await bot.send_poll(
        chat_id=CHAT_ID,
        question=f"🎲 Viikon {week_number} pelipäivät | Week {week_number} game sessions?",
        options=options,
        is_anonymous=False,
        allows_multiple_answers=True,
        type="regular",
        protect_content=False,
        close_date=close_date
    )

    print(f"Poll sent for week {week_number}")