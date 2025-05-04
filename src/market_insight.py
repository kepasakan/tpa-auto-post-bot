import os
import google.generativeai as genai
from datetime import datetime
from telegram import Bot
import asyncio

# Load local .env only if not running in GitHub Actions
if not os.getenv("GITHUB_ACTIONS"):
    from dotenv import load_dotenv
    load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Format today's date (e.g., 4 Mei 2025)
today = datetime.now().strftime('%#d %B %Y') # Malay-style format

# Telegram bot setup
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
bot = Bot(token=BOT_TOKEN)

# Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Prompt with today's date
prompt = f"""
Bertindak sebagai seorang penganalisis pasaran profesional dan jurulatih dagangan yang pakar dalam menyampaikan sentimen pasaran harian untuk pedagang forex, komoditi, dan indeks.

Hari ini adalah: **{today}**

Tugas anda adalah untuk menghasilkan laporan pasaran harian dalam format **penuh seperti di bawah**, untuk diposkan ke saluran Telegram. Laporan ini mesti berdasarkan:

- Data ekonomi berimpak tinggi (NFP, CPI, FOMC, PMI)
- Fundamental global semasa (pilihan raya AS, inflasi, Fed, ECB, China, geopolitik)
- Kenyataan bank pusat atau tokoh penting (contoh: Trump, Powell, Lagarde)
- Reaksi semasa pasaran (volatiliti, risk-on/risk-off, aliran modal)

**Arahan Format:**
Gunakan format yang TETAP dan TEPAT seperti di bawah (jangan ubah struktur atau urutan):

📊 Market Insight - {today}

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

response = model.generate_content(prompt)
message = f"📊 *Market Insight - {today}*\n\n{response.text}"

# Send to Telegram
async def send_to_telegram():
    await bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(send_to_telegram())