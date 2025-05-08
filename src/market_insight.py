import os
import asyncio
from datetime import datetime, timedelta, timezone
from telegram import Bot
from telegram.error import TimedOut
from openai import OpenAI
import requests

# Load .env if not running in GitHub Actions
if not os.getenv("GITHUB_ACTIONS"):
    from dotenv import load_dotenv
    load_dotenv()

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# Setup clients
client = OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=BOT_TOKEN)

# ✅ Fetch headlines based on hour range & count
def fetch_market_headlines(hours=24, count=5):
    now = datetime.now(timezone.utc)
    from_time = (now - timedelta(hours=hours)).isoformat()

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=Fed OR FOMC OR Trump OR inflation OR Powell OR CPI OR ECB OR Gold OR Dollar OR China OR rate hike "
        f"&from={from_time}&sortBy=popularity&language=en"
        f"&apiKey={NEWSAPI_KEY}"
    )

    response = requests.get(url)
    articles = response.json().get("articles", [])

    top_headlines = []
    for article in articles[:count]:
        title = article.get("title")
        source = article.get("source", {}).get("name")
        if title and source:
            top_headlines.append(f"- {title} ({source})")

    if not top_headlines:
        top_headlines.append("- Tiada berita penting ditemui dalam tempoh ini.")

    return "\n".join(top_headlines)

# Get today's date
today = datetime.now().strftime('%#d %B %Y')

# 🔹 Top 5 in 24 hours
top_news_24h = fetch_market_headlines(hours=24, count=5)

# 🔹 Top 20 in past 5 days
top_news_5d_raw = fetch_market_headlines(hours=120, count=20)
top_news_5d = "\n".join([f"{i+1}. {line}" for i, line in enumerate(top_news_5d_raw.splitlines())])

# 🔹 Final prompt
prompt = f"""
📌 Anda diberikan dua senarai berita utama berdasarkan populariti:

🕒 **5 berita paling popular dalam 24 jam terakhir:**
{top_news_24h}

🗓️ **20 berita paling popular dalam 5 hari terakhir:**
{top_news_5d}

Gunakan kedua-dua senarai ini untuk menulis laporan pasaran harian secara lengkap dan menyeluruh.

Hari ini adalah: **{today}**

🔥 Poin Utama:  
Senaraikan **5 cerita utama pasaran** hari ini (gunakan nombor 1–5), berdasarkan berita di atas.

🌍 Sentimen Pasaran:  
1 perenggan pendek yang merumuskan mood pasaran secara keseluruhan (risk-on, risk-off, bercampur, berhati-hati), berdasarkan berita.

__________________________________________________________

📊 Sorotan Mata Wang & Komoditi:

- USD: [Bullish/Bearish/Bercampur] – 1 ayat berdasarkan berita.
- EUR: ...
- GBP: ...
- JPY: ...
- AUD: ...
- NZD: ...
- CAD: ...
- CHF: ...

Komoditi :-

- XAUUSD (Emas): [Bullish/Bearish/Bercampur] – Penjelasan 1 ayat.
- WTI (Minyak Mentah): [Bullish/Bearish/Bercampur] – Penjelasan 1 ayat.

Indeks :-

- NAS100: [Bullish/Bearish/Bercampur] – Penjelasan 1 ayat.
- SPX500: [Bullish/Bearish/Bercampur] – Penjelasan 1 ayat.

__________________________________________________________

💬 Tip Psikologi Hari Ini:  
1 ayat nasihat mindset/psikologi/risk control berdasarkan keadaan pasaran hari ini.
"""

# 🔹 Generate insight using OpenAI
def generate_insight():
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Anda adalah pakar analisis pasaran profesional."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1800,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# 🔹 Send to Telegram
async def send_to_telegram():
    response_text = generate_insight()
    message = f"📊 *Market Insight - {today}*\n\n{response_text}"
    try:
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode='Markdown')
    except TimedOut:
        print("⚠️ Telegram API timed out. Cek connection atau cuba semula.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# 🔹 Run
if __name__ == "__main__":
    asyncio.run(send_to_telegram())
