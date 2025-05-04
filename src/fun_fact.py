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
Bertindak sebagai seorang guru dagangan yang menyeronokkan, profesional dan berpengetahuan luas. Tugas anda adalah untuk menghasilkan *1 fakta menarik, pelik, atau mengejutkan* berkaitan dunia dagangan seperti forex, saham, kripto, atau indeks.

Hari ini ialah: **{today}**

✅ Fakta mesti:
- Berdasarkan fakta sebenar (bukan fiksyen)
- Mengejutkan, jarang diketahui, atau mind-blown untuk trader
- Sesuai untuk beginner atau prop trader — *bukan terlalu teknikal*
- Ditulis dalam gaya bahasa santai, penuh karakter, dan mudah difahami
- Disampaikan dalam **2 perenggan pendek sahaja** untuk mudah dibaca di Telegram
- Sertakan nombor/angka real jika sesuai

✅ Format output WAJIB seperti ini:

🎉 **Fun Fact Trading Hari Ini**  
🧠 *[Tajuk mini catchy di sini]*

[Perenggan 1: Buka dengan ayat punchy atau persoalan menarik — terus kepada fakta unik tersebut. Gunakan emoji dengan bijak, caps lock untuk penekanan, dan bold untuk highlight angka atau point penting.]

[Perenggan 2: Ajak pembaca berfikir atau bandingkan situasi dengan konteks dagangan hari ini. Boleh letak unsur humor, refleksi, atau cabaran berfikir.]

Akhiri dengan **1–2 emoji** dan **hashtag** (pilih ikut topik):  
`#ForexFun #MindBlown #CryptoCrazy #TimeTravelTrading #TraderLife`

Contoh gaya:
🎉 **Fun Fact Dagangan Hari Ini (05/05/2025)**  
🧠 *Pizza vs Bitcoin: Pilihan Siapa Lagi Berbaloi?*

Kalau anda belanja $100 untuk pizza tahun 2010 🍕, kenyang sehari. Tapi kalau anda laburkan $100 untuk beli Bitcoin masa tu (harga bawah $0.01!) dan HODL sampai sekarang... anda mungkin dah ada **lebih $500 juta** hari ini! 😵‍💫🚀

Bezanya hanya satu keputusan — makan sekarang, atau sabar & biar duit bekerja. Jadi... nak belanja kopi lagi hari ni, atau simpan untuk future portfolio? 😉  
#CryptoCrazy #MindBlown

Tugas anda hari ini adalah hasilkan **1 fun fact unik dan berformat seperti di atas** ber.
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
