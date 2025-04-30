from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from telegram.error import TelegramError
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')

bot = Bot(token=BOT_TOKEN)

async def setup_scheduler(calendar_job, motivation_job):
    """Setup and start the scheduler with the given jobs."""
    scheduler = AsyncIOScheduler()
    
    # Schedule calendar posts at 00:01 daily
    scheduler.add_job(calendar_job, 'cron', hour=0, minute=1)
    
    # Schedule motivation posts at 07:00 daily
    scheduler.add_job(motivation_job, 'cron', hour=7, minute=0)
    
    scheduler.start()
    return scheduler

async def send_message(message):
    """Send a message to the configured group chat."""
    try:
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode='Markdown')
    except TelegramError as e:
        logging.error(f'Telegram error: {e}')
    except Exception as e:
        logging.error(f'Failed to send message: {e}')

async def test_telegram_connection():
    """Test the Telegram bot connection."""
    try:
        logging.info('Testing Telegram connection...')
        bot_info = await bot.get_me()
        logging.info(f'Successfully connected to Telegram as @{bot_info.username}')
        return True
    except Exception as e:
        logging.error(f'Failed to connect to Telegram: {e}')
        return False 