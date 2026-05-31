import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

async def main():
    async with Bot(BOT_TOKEN) as bot:
        await bot.send_message(
            chat_id=CHAT_ID,
            text="Botti testi"
        )

asyncio.run(main())