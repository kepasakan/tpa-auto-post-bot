import logging
import requests

async def fetch_motivation_quote():
    """Fetch a random motivational quote from zenquotes.io."""
    try:
        logging.info('Starting to fetch motivation quote...')
        quote_res = requests.get('https://zenquotes.io/api/random')
        logging.info(f'Quote API response status: {quote_res.status_code}')
        
        if quote_res.status_code == 200:
            quote_data = quote_res.json()
            return {
                'text': quote_data[0]['q'],
                'author': quote_data[0]['a']
            }
        else:
            return None
    except Exception as e:
        logging.error(f'Failed to fetch motivation quote: {e}')
        return None

def format_motivation_message(quote_data):
    """Format the quote into a message."""
    if quote_data:
        return f'🌟 **Motivation of the Day**\n\n"{quote_data["text"]}"\n\n- _{quote_data["author"]}_'
    else:
        return '🌟 Stay motivated and disciplined, Trader!' 