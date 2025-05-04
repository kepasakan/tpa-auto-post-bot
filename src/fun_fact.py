import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from telegram import Bot
import asyncio

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Get today's date for the prompt
today = datetime.now().strftime('%d/%m/%Y')

# Prepare Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Prompt to generate a trading-related fun fact with today's date
prompt = f"""
Bertindak sebagai seorang guru dagangan yang menyeronokkan dan berpengetahuan luas. Tugas anda adalah untuk memberikan *1 fakta menarik, pelik, atau mengejutkan* berkaitan dunia dagangan seperti forex, saham, kripto, atau indeks.

Hari ini ialah: **{today}**

✅ Fakta mesti:
- Mengejutkan, jarang diketahui, atau kelakar
- Berdasarkan fakta sebenar dan relevan untuk trader
- Ditulis dalam gaya bahasa santai, mudah difahami, dan ada unsur hiburan
- Disampaikan dalam 1 perenggan sahaja
- Sesuai untuk dipos ke Telegram

✅ Format output WAJIB seperti ini:

🎉 **Fun Fact Dagangan Hari Ini ({today})**

[1 perenggan fakta penuh di sini, gaya santai, gunakan emoji, bold untuk highlight bahagian menarik, caps lock untuk tekan perkataan penting, dan gunakan ayat yang ajak trader berfikir.]

Akhiri dengan 1–2 emoji dan hashtag (seperti `#ForexFun`, `#MindBlown`, `#TradingFact`, dll.)

Contoh gaya penulisan:
"Woi trader! 😱 Tahu tak, kalau kita gabungkan SEMUA duit fizikal kat dunia ni, jumlahnya cuma $8 trilion je... tapi nilai pasaran forex **SETIAP HARI** boleh cecah lebih $7.5 trilion! 😵‍💫 Fikirkan tu!"

Tugas anda hari ini adalah hasilkan **1 fun fact unik dan berformat seperti di atas** berdasarkan tarikh `{today}`.
"""

# Define async function
async def main():
    response = model.generate_content(prompt)
    fact = response.text.strip()
    message = fact  # fact already includes the heading with date

    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode='Markdown')

# Run async
if __name__ == "__main__":
    asyncio.run(main())
