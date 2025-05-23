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

def fetch_market_headlines_24h(count=30):  # ⬅️ count = 30
    now = datetime.now(timezone.utc)
    from_time = (now - timedelta(hours=24)).isoformat()
    to_time = now.isoformat()

    economic_sources = (
        "bloomberg.com,reuters.com,cnbc.com,ft.com,economist.com,"
        "marketwatch.com,wsj.com,investing.com,forexlive.com"
    )

    url = (
        f"https://newsapi.org/v2/everything?"
        f"from={from_time}&to={to_time}&sortBy=publishedAt&language=en"  # ⬅️ Use publishedAt instead of popularity
        f"&domains={economic_sources}"
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

# 🔹 Top 20 in 24 hours
top_news_24h = fetch_market_headlines_24h(count=20)
print("✅ Top News 24H:\n", top_news_24h)

# 🔹 Final prompt
prompt = f"""
📌 Berikut ialah **30 berita terbaru dalam 24 jam terakhir** daripada sumber ekonomi terpilih:

🕒 **30 Headline Ekonomi Terkini (24 Jam):**
{top_news_24h}

Gunakan kedua-dua senarai ini untuk menulis laporan pasaran harian secara lengkap dan menyeluruh.

🔥 Poin Utama:  
Senaraikan **5 cerita utama pasaran yang informatif dan berguna sahaja untuk trading** hari ini (gunakan nombor 1–5), berdasarkan berita di atas. (Jarakkan setiap point untuk ada spacing sikit)

🌍 Sentimen Pasaran:  
1 perenggan pendek yang merumuskan mood pasaran secara keseluruhan (risk-on, risk-off, bercampur, berhati-hati), berdasarkan berita.

__________________________________________________________

📊 Sorotan Mata Wang & Komoditi:

💵 Mata Wang:
- **USD** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]
- **EUR** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]
- **GBP** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]
- **JPY** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]
- **AUD** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]
- **NZD** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]
- **CAD** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]
- **CHF** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]

🛢 Komoditi:
- **XAUUSD (Emas)** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]
- **WTI (Minyak)** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]

📈 Indeks:
- **NAS100** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]
- **SPX500** → [📈 Bullish / 📉 Bearish / 📊 Bercampur] — [1 ayat sebab]

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


