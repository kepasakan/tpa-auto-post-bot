# TPA Auto-Post Bot

A Telegram bot that automatically posts forex calendar events and motivational quotes to a specified group chat.

## Features

- Posts daily forex calendar events with high and medium impact
- Posts daily motivational quotes
- Automatic scheduling of posts
- Timezone conversion for KL time (GMT+8)

## Project Structure

```
tpa-auto-post-bot/
├── src/
│   ├── __init__.py
│   ├── bot.py
│   ├── calendar.py
│   ├── motivation.py
│   └── scheduler.py
├── tests/
│   └── __init__.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your credentials:
   ```
   BOT_TOKEN=your_telegram_bot_token
   GROUP_CHAT_ID=your_group_chat_id
   ```

## Usage

Run the bot:
```bash
python -m src.bot
```

## License

MIT License
