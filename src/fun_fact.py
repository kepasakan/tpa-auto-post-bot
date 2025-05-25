import os
import asyncio
from datetime import datetime
from telegram import Bot
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ENV VARS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_FUN_FACT")  # use your new working key
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID_FUN = os.getenv("GROUP_CHAT_ID_FUN")

# Setup OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Setup Telegram bot
bot = Bot(token=BOT_TOKEN)

# Get today's date
today = datetime.now().strftime('%d/%m/%Y')

# Prompt for fun fact
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

✅ Output WAJIB ditulis dalam **Bahasa Melayu** sepenuhnya.

✅ Format output WAJIB seperti ini:

🎉 **Fun Fact Trading Hari Ini**  
🧠 *[Tajuk mini catchy di sini]*

[Perenggan 1: Buka dengan ayat punchy atau persoalan menarik — terus kepada fakta unik tersebut. Gunakan emoji dengan bijak, caps lock untuk penekanan, dan bold untuk highlight angka atau point penting.]

[Perenggan 2: Ajak pembaca berfikir atau bandingkan situasi dengan konteks dagangan hari ini. Boleh letak unsur humor, refleksi, atau cabaran berfikir.]

Akhiri dengan **1–2 emoji** dan **hashtag** (pilih ikut topik):  
`#ForexFun #MindBlown #CryptoCrazy #TimeTravelTrading #TraderLife`

Contoh gaya:
🎉 **Fun Fact Dagangan Hari Ini**  
🧠 *Pizza vs Bitcoin: Pilihan Siapa Lagi Berbaloi?*

Kalau anda belanja $100 untuk pizza tahun 2010 🍕, kenyang sehari. Tapi kalau anda laburkan $100 untuk beli Bitcoin masa tu (harga bawah $0.01!) dan HODL sampai sekarang... anda mungkin dah ada **lebih $500 juta** hari ini! 😵‍💫🚀

Bezanya hanya satu keputusan — makan sekarang, atau sabar & biar duit bekerja. Jadi... nak belanja kopi lagi hari ni, atau simpan untuk future portfolio? 😉  
#CryptoCrazy #MindBlown

Tugas anda hari ini adalah hasilkan **1 fun fact unik dan berformat seperti di atas**, dalam Bahasa Melayu, berdasarkan fakta sebenar.
"""

# Generate fun fact using OpenAI
def generate_fun_fact():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if accessible
        messages=[
            {"role": "system", "content": "Anda adalah guru dagangan yang menyeronokkan dan suka berkongsi fakta menarik."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.9,
    )
    return response.choices[0].message.content.strip()

# Send to Telegram
async def main():
    fact = generate_fun_fact()
    await bot.send_message(chat_id=GROUP_CHAT_ID_FUN, text=fact, parse_mode='Markdown')

# Run
if __name__ == "__main__":
    asyncio.run(main())
