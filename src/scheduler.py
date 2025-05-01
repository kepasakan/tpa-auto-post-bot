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