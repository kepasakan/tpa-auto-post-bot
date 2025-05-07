import os
import asyncio
from datetime import datetime
from telegram import Bot
from openai import OpenAI

# Load .env if not running in GitHub Actions
if not os.getenv("GITHUB_ACTIONS"):
    from dotenv import load_dotenv
    load_dotenv()

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Setup OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Setup Telegram bot
bot = Bot(token=BOT_TOKEN)

# Get today's date
today = datetime.now().strftime('%#d %B %Y')

# Prompt for daily market insight
prompt = f"""
Bertindak sebagai seorang penganalisis pasaran profesional dan jurulatih dagangan yang pakar dalam menyampaikan sentimen pasaran harian untuk pedagang forex, komoditi, dan indeks.

Hari ini adalah: **{today}**

Tugas anda adalah untuk menghasilkan laporan pasaran harian dalam format **penuh seperti di bawah**, untuk diposkan ke saluran Telegram. Laporan ini mesti berdasarkan:

- Data ekonomi berimpak tinggi (NFP, CPI, FOMC, PMI)
- Fundamental global semasa (pilihan raya AS, inflasi, Fed, ECB, China, geopolitik)
- Kenyataan bank pusat atau tokoh penting (contoh: Trump, Powell, Lagarde)
- Reaksi semasa pasaran (volatiliti, risk-on/risk-off, aliran modal)

**Arahan Format:**
Gunakan format yang TETAP dan TEPAT seperti di bawah. **WAJIB masukkan garisan pemisah (__________________________________________________________) selepas Sentimen Pasaran dan sebelum Tip Psikologi. Jangan abaikan atau ubah format struktur ini.**

🔥 Poin Utama:  
Senaraikan **5 cerita utama pasaran** hari ini (gunakan nombor 1–5), termasuk geopolitik, ekonomi, bank pusat, atau sebarang catalyst utama.

🌍 Sentimen Pasaran:  
Satu perenggan pendek tentang mood pasaran secara keseluruhan (risk-on, risk-off, bercampur, berhati-hati). Nyatakan kenapa pasaran dalam mood itu.

__________________________________________________________

📊 Sorotan Mata Wang & Komoditi:

- USD: [Bullish/Bearish/Bercampur] – Penjelasan 1 ayat sebab kenapa.
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

# Generate insight using OpenAI
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

# Send the response to Telegram
async def send_to_telegram():
    response_text = generate_insight()
    message = f"📊 *Market Insight - {today}*\n\n{response_text}"
    await bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode='Markdown')

# Run the async function
if __name__ == "__main__":
    asyncio.run(send_to_telegram())
