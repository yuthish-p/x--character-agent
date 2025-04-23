import schedule
import time
import asyncio
from config import Config
from utils.logger import logger
from agent import main  


def run_async_main():
    loop = asyncio.get_event_loop()
    loop.create_task(main())  

def schedule_tasks():
    schedule.every(Config.TWITTER_POST_INTERVAL).minutes.do(run_async_main)  # Safe async execution
    logger.info(f"Scheduled social media posts every {Config.TWITTER_POST_INTERVAL} seconds.")

async def run_scheduler():
    schedule_tasks()
    logger.info("Starting the scheduler...")
    
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)  

# Start the script
if __name__ == "__main__":
    asyncio.run(run_scheduler())  
