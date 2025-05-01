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

    # Run the appropriate function based on the time
    # This will be determined by the GitHub Actions workflow
    import sys
    if len(sys.argv) > 1:
        job_type = sys.argv[1]
        if job_type == 'calendar':
            await post_forex_calendar()
        elif job_type == 'motivation':
            await post_motivation()
        else:
            logging.error(f'Unknown job type: {job_type}')
    else:
        logging.error('No job type specified')

if __name__ == '__main__':
    asyncio.run(main()) 