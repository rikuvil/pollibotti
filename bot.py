import os
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
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
    # 1. Set to Finland timezone
    helsinki_tz = ZoneInfo("Europe/Helsinki")
    now = datetime.now(helsinki_tz)

    # 2. Advance by 7 days to target next week
    next_week_target = now + timedelta(days=7)
    
    # 3. Calculate next week's ISO week number
    week_number = next_week_target.isocalendar()[1]
    
    # 4. Calculate next week's Monday date 
    # (Forces the target to snap back to the Monday of that next week)
    next_monday = next_week_target - timedelta(days=next_week_target.weekday())

    # English -> Suomi päivät
    options = []
    for i in range(7):
        day = next_monday + timedelta(days=i)
        weekday = FI_WEEKDAYS[i]
        date_str = day.strftime("%d.%m")
        options.append(f"{weekday} {date_str}")

    # Extra vastaukset
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
    print(f"Poll for week {week_number} successfully sent at {datetime.now(helsinki_tz)}")

async def main():
    helsinki_tz = ZoneInfo("Europe/Helsinki")
    scheduler = AsyncIOScheduler(timezone=helsinki_tz)
    
    # Uus polli sunnuntaisin klo 20:00 seuraavalle viikolle.
    scheduler.add_job(
        send_weekly_poll,
        trigger='cron',
        day_of_week='sun', 
        hour=12,
        minute=00
    )
    scheduler.start()
    print("Bot scheduler running strictly on Europe/Helsinki time...")
    print("Next poll will automatically send this Sunday at 20:00.")
    
    # Keep the async loop alive indefinitely
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nBot stopped.")