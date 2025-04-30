import logging
import asyncio
from . import calendar
from . import motivation
from . import scheduler

# Configure logging
logging.basicConfig(level=logging.INFO)

async def post_forex_calendar():
    """Post today's forex calendar events."""
    try:
        xml_content = await calendar.fetch_forex_calendar()
        events = calendar.parse_forex_calendar(xml_content)
        message = calendar.format_calendar_message(events)
        await scheduler.send_message(message)
        logging.info('Posted Forex Calendar.')
    except Exception as e:
        logging.error(f'Calendar posting failed: {e}')

async def post_motivation():
    """Post a motivational quote."""
    try:
        quote_data = await motivation.fetch_motivation_quote()
        message = motivation.format_motivation_message(quote_data)
        await scheduler.send_message(message)
        logging.info('Posted Motivation.')
    except Exception as e:
        logging.error(f'Motivation posting failed: {e}')

async def main():
    """Main function to run the bot."""
    # Test Telegram connection
    if not await scheduler.test_telegram_connection():
        logging.error('Cannot start bot due to Telegram connection issues')
        return

    # Setup scheduler
    scheduler_obj = await scheduler.setup_scheduler(post_forex_calendar, post_motivation)
    print('TPA Auto-Post Bot is running...')

    # TEMPORARY TEST POST (Manual Trigger)
    logging.info('Starting test posts...')
    await post_forex_calendar()
    await post_motivation()

    # Keep alive loop
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler_obj.shutdown()
        print('Bot stopped.')

if __name__ == '__main__':
    asyncio.run(main()) 