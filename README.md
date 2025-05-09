# 🤖 TPA Auto-Post Bot

This project automates daily **Forex trading content posting** to a Telegram channel using:
- 🧠 Gemini AI (Google Generative AI)
- 📆 Forex Economic Calendar
- 💡 Trading Motivation & Psychology Tips

## 📌 Features

| Bot Type           | Description                                                                 | Schedule (MYT) |
|--------------------|-----------------------------------------------------------------------------|----------------|
| 🧠 Market Insight  | Auto-generates daily market analysis using Gemini AI                        | 6:00 AM        |
| 📆 Forex Calendar  | Sends upcoming economic news and impact for the trading day                 | 1:00 AM        |
| 💬 Motivation Tip  | Sends a motivational message or trading mindset tip                         | 6:00 AM        |

---

## 🗂 Folder Structure

```
tpa-auto-post-bot/
├── .github/workflows/
│ ├── calendar-post.yml # Triggers forex calendar bot
│ ├── market-insight.yml # Triggers Gemini market insight bot
│ └── motivation-post.yml # Triggers daily motivation bot
│
├── src/
│ ├── bot.py # Handles job routing & Telegram logic
│ ├── market_insight.py # Gemini AI market insight logic
│ ├── forex_calendar.py # Forex news fetcher
│ ├── motivation.py # Daily mindset tip logic
│ ├── scheduler.py # Internal dispatcher
│
├── .env # Local environment variables (ignored by Git)
├── env.example # Template for .env file
├── requirements.txt # All Python dependencies
└── README.md
```


---

## 🔐 Environment Variables

Create a `.env` file based on the `env.example` file and set your values:

- BOT_TOKEN=your_telegram_bot_token
- GROUP_CHAT_ID=your_telegram_group_id
- GEMINI_API_KEY=your_google_generative_ai_key


> ⚠️ These are required for the bots to function properly.

---

## 🚀 GitHub Actions Automation

Each bot runs via its own **`.yml` file** inside `.github/workflows/`. Example:

- **Market Insight**: `.github/workflows/market-insight.yml`
- **Motivation**: `.github/workflows/motivation-post.yml`
- **Forex Calendar**: `.github/workflows/calendar-post.yml`

These run automatically based on the cron schedule, or you can trigger them manually via the GitHub Actions UI.

---

## 🧠 Gemini AI Integration

This project uses `google.generativeai` to generate rich market content.  
Model used: `gemini-1.5-pro-latest`.

---

## ✅ To Do Next

- [x] Fix Gemini API integration
- [x] Auto-send to Telegram
- [ ] Add error handling & logging
- [ ] Add support for image posts (future)

---

## 👨‍💻 Made with ❤️ by Trader Prop Academy

Follow for more automated trading tools and strategies
