from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from zoneinfo import ZoneInfo
from poll_system import send_weekly_poll
from state import has_run_this_week, mark_run

scheduler = AsyncIOScheduler()

# Job to send weekly poll and mark it as run in state as week number
async def job():
    now = datetime.now(ZoneInfo("Europe/Helsinki"))
    week_key = f"{now.isocalendar().year}-{now.isocalendar().week}"

    if has_run_this_week(week_key):
        print(f"Skipping duplicate poll for {week_key}")
        return

    await send_weekly_poll()
    mark_run(week_key)

# Starts it or something 
def start_scheduler():
    scheduler.configure(timezone=ZoneInfo("Europe/Helsinki"))
    scheduler.add_job(job, "cron", day_of_week="sun", hour=16, minute=00)
    scheduler.start()
    print("Scheduler started successfully! Weekly poll set for Sundays.")
