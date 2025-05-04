import logging
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

async def fetch_forex_calendar():
    """Fetch and parse forex calendar events."""
    try:
        logging.info('Starting to fetch forex calendar...')
        url = 'https://nfs.faireconomy.media/ff_calendar_thisweek.xml'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch calendar. Status code: {response.status_code}")
        
        return response.content
    except Exception as e:
        logging.error(f'Failed to fetch calendar: {e}')
        raise

def parse_forex_calendar(xml_content):
    """Parse XML content and return formatted events for the next UTC day."""
    root = ET.fromstring(xml_content)
    
    # Set target to tomorrow's date in UTC
    tomorrow_utc = datetime.utcnow().date() + timedelta(days=1)
    target_date_str = tomorrow_utc.strftime('%m-%d-%Y')
    
    events = []

    for event in root.findall('.//event'):
        date_str = event.find('date').text.strip()
        time_str = event.find('time').text.strip()
        impact = event.find('impact').text if event.find('impact') is not None else 'Low'

        if impact.lower() not in ['high', 'medium']:
            continue
        
        # ✅ Only continue if event is for tomorrow's UTC date
        if date_str != target_date_str:
            continue

        # Parse and convert to KL time
        try:
            event_time = datetime.strptime(time_str, '%I:%M%p').time()
            event_date = datetime.strptime(date_str, '%m-%d-%Y').date()
            event_datetime_utc = datetime.combine(event_date, event_time)
            kl_datetime = event_datetime_utc + timedelta(hours=8)
            formatted_time = kl_datetime.strftime('%I:%M %p')
        except ValueError as e:
            logging.error(f"Time parsing error: {e}")
            formatted_time = time_str
        
        title = event.find('title').text
        country = event.find('country').text
        forecast = event.find('forecast').text if event.find('forecast') is not None else 'N/A'
        previous = event.find('previous').text if event.find('previous') is not None else 'N/A'

        event_text = f"⏰ {formatted_time}\n"
        event_text += f"🌍 {country}: {title}\n"
        if forecast != 'N/A':
            event_text += f"📊 Forecast: {forecast}\n"
        if previous != 'N/A':
            event_text += f"📈 Previous: {previous}\n"
        event_text += f"Impact: {'🔴 HIGH' if impact.lower() == 'high' else '🟡 MEDIUM'}\n"

        events.append((kl_datetime, impact.lower(), event_text))
    
    return events


def format_calendar_message(events):
    """Format the calendar events into a message."""
    now = datetime.now()
    message = "🚨 *Today's Important Forex Events*\n\n"
    
    if not events:
        message += 'No important events today. Trade safe! 🛡️'
    else:
        # Sort events by time, but put HIGH impact first for same time
        events.sort(key=lambda x: (x[0], 0 if x[1] == 'high' else 1))
        today_events = [event[2] for event in events]
        
        message += f"Date: {now.strftime('%A, %B %d, %Y')}\n\n"
        message += '\n'.join(today_events)
        message += "\n\n⚠️ All times are in KL time (GMT+8)"
    
    return message 