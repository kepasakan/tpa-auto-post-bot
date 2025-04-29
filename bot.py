import logging
import requests
import os
import asyncio
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')

# Debug logging for environment variables
if not BOT_TOKEN:
    logging.error('BOT_TOKEN is not set in environment variables')
if not GROUP_CHAT_ID:
    logging.error('GROUP_CHAT_ID is not set in environment variables')

bot = Bot(token=BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

async def post_forex_calendar():
    try:
        logging.info('Starting to fetch forex calendar...')
        url = 'https://nfs.faireconomy.media/ff_calendar_thisweek.xml'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch calendar. Status code: {response.status_code}")
        
        # Parse XML
        root = ET.fromstring(response.content)
        message = "🚨 *Today's Important Forex Events*\n\n"
        
        # Get current date for filtering today's events
        now = datetime.now()
        today = now.strftime('%m-%d-%Y')
        
        events = []
        for event in root.findall('.//event'):
            date_str = event.find('date').text.strip()
            time_str = event.find('time').text.strip()
            impact = event.find('impact').text if event.find('impact') is not None else 'Low'
            
            # Only include High and Medium impact
            if impact.lower() not in ['high', 'medium']:
                continue
                
            # Skip if not today's date
            if date_str != today:
                continue
            
            # Parse event datetime and add 8 hours for KL time
            try:
                # Parse the base time (which is in EST)
                event_time = datetime.strptime(time_str, '%I:%M%p').time()
                event_date = datetime.strptime(date_str, '%m-%d-%Y').date()
                event_datetime = datetime.combine(event_date, event_time)
                
                # Add 8 hours for KL time
                kl_datetime = event_datetime + timedelta(hours=8)
                
                # Format for display
                formatted_time = kl_datetime.strftime('%I:%M %p')  # e.g., "10:00 PM"
            except ValueError as e:
                logging.error(f"Time parsing error: {e}")
                formatted_time = time_str
            
            title = event.find('title').text
            country = event.find('country').text
            forecast = event.find('forecast').text if event.find('forecast') is not None else 'N/A'
            previous = event.find('previous').text if event.find('previous') is not None else 'N/A'
            
            # Format the event information
            event_text = f"⏰ {formatted_time}\n"
            event_text += f"🌍 {country}: {title}\n"
            if forecast and forecast != 'N/A':
                event_text += f"📊 Forecast: {forecast}\n"
            if previous and previous != 'N/A':
                event_text += f"📈 Previous: {previous}\n"
            # Use red for high impact, orange for medium
            event_text += f"Impact: {'🔴 HIGH' if impact.lower() == 'high' else '🟡 MEDIUM'}\n"
            events.append((kl_datetime, impact.lower(), event_text))
        
        # Sort events by time, but put HIGH impact first for same time
        events.sort(key=lambda x: (x[0], 0 if x[1] == 'high' else 1))
        today_events = [event[2] for event in events]
        
        if not today_events:
            message += 'No important events today. Trade safe! 🛡️'
        else:
            message += f"Date: {now.strftime('%A, %B %d, %Y')}\n\n"
            message += '\n'.join(today_events)
            message += "\n\n⚠️ All times are in KL time (GMT+8)"
            
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode='Markdown')
        logging.info('Posted Forex Calendar.')
    except TelegramError as e:
        logging.error(f'Telegram error: {e}')
    except Exception as e:
        logging.error(f'Calendar posting failed: {e}')
        logging.error(f'Error details: {str(e)}')

async def post_motivation():
    try:
        logging.info('Starting to fetch motivation quote...')
        quote_res = requests.get('https://zenquotes.io/api/random')
        logging.info(f'Quote API response status: {quote_res.status_code}')
        if quote_res.status_code == 200:
            quote_data = quote_res.json()
            quote_text = quote_data[0]['q']
            quote_author = quote_data[0]['a']
            message = f'🌟 **Motivation of the Day**\n\n"{quote_text}"\n\n- _{quote_author}_'
        else:
            message = '🌟 Stay motivated and disciplined, Trader!'
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode='Markdown')
        logging.info('Posted Motivation.')
    except TelegramError as e:
        logging.error(f'Telegram error: {e}')
    except Exception as e:
        logging.error(f'Motivation posting failed: {e}')

async def test_telegram_connection():
    try:
        logging.info('Testing Telegram connection...')
        # Try to get bot info to verify connection
        bot_info = await bot.get_me()
        logging.info(f'Successfully connected to Telegram as @{bot_info.username}')
        return True
    except Exception as e:
        logging.error(f'Failed to connect to Telegram: {e}')
        return False

async def main():
    # Scheduler Setup
    scheduler = AsyncIOScheduler()
    scheduler.add_job(post_forex_calendar, 'cron', hour=0, minute=1)
    scheduler.add_job(post_motivation, 'cron', hour=7, minute=0)
    scheduler.start()

    print('TPA Auto-Post Bot is running...')

    # TEMPORARY TEST POST (Manual Trigger)
    if await test_telegram_connection():
        logging.info('Starting test posts...')
        await post_forex_calendar()
        await post_motivation()
    else:
        logging.error('Cannot proceed with test posts due to Telegram connection issues')

    # Keep alive loop
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Bot stopped.')

if __name__ == '__main__':
    asyncio.run(main())