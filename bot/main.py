import asyncio
from scheduler import start_scheduler, job

async def main():
    print("Bot starting...")
    start_scheduler()
    print("Scheduler started")
    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        print("Shutting down...")

        
if __name__ == "__main__":
    asyncio.run(main())