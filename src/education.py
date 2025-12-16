import os
import asyncio
from datetime import datetime
from telegram import Bot
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ENV VARS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_FUN_FACT")  # Reusing the existing key variable or you can create a new one
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID_EDUCATION = os.getenv("GROUP_CHAT_ID_EDUCATION")  # Make sure to add this to your .env file

# Setup OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Setup Telegram bot
bot = Bot(token=BOT_TOKEN)

# Get today's date and day
now = datetime.now()
today_date = now.strftime('%d/%m/%Y')
day_name = now.strftime('%A')

# Define topics based on day
topics = {
    "Monday": {
        "title": "Market Outlook & Setup",
        "focus": "Merangka Watchlist mingguan, semak kalendar ekonomi (Forex Factory), dan merancang pair mana yang akan difokuskan."
    },
    "Tuesday": {
        "title": "Seni Pengurusan Risiko (Risk Management)",
        "focus": "Cara kira lot size yang tepat, memahami Daily Drawdown vs Max Drawdown, dan kenapa 'Stop Loss' itu wajib dalam prop firm."
    },
    "Wednesday": {
        "title": "Psikologi & Emosi (Mid-Week Mindset)",
        "focus": "Mengawal FOMO, menangani losing streak, dan bagaimana untuk tidak balas dendam (revenge trade) selepas terkena SL."
    },
    "Thursday": {
        "title": "Strategi Teknikal & SOP",
        "focus": "Kupasan satu teknik spesifik (contoh: SMC, SNR, atau Price Action), entry confirmation, dan masa terbaik untuk entry."
    },
    "Friday": {
        "title": "Review & Journaling",
        "focus": "Melakukan post-mortem trade minggu ini. Apa yang jadi? Apa yang salah? Adakah SOP dipatuhi?"
    },
    "Saturday": {
        "title": "Pemahaman Peraturan Prop Firm (The Rules)",
        "focus": "Topik teknikal tentang prop firm seperti News Trading rules, Holding over weekend, IP address issues, atau perbezaan antara HFT dan manual trading."
    },
    "Sunday": {
        "title": "Rehat & Reset Minda",
        "focus": "Pentingnya hobi di luar chart, tidur yang cukup, dan persediaan mental untuk minggu hadapan."
    }
}

current_topic = topics.get(day_name, topics["Monday"])  # Default to Monday if something fails

# Prompt for education tip
prompt = f"""
Bertindak sebagai seorang mentor dagangan yang berpengalaman, bijak, dan sangat membantu. Tugas anda adalah untuk menghasilkan *1 tips pendidikan, panduan, atau nasihat dagangan* yang bernilai tinggi berkaitan dunia dagangan seperti forex, saham, kripto, atau indeks.

Hari ini ialah: **{day_name}, {today_date}**
Topik Hari Ini: **{current_topic['title']}**
Fokus Utama: **{current_topic['focus']}**

✅ Tips mesti:
- Berdasarkan prinsip dagangan yang betul (teknikal, fundamental, atau psikologi) sesuai dengan topik di atas.
- Memberikan nilai tambah kepada trader (beginner atau intermediate)
- *Bukan signal buy/sell*, tetapi ilmu atau nasihat
- Ditulis dalam gaya bahasa profesional tetapi mudah difahami (santai)
- Disampaikan dalam **2-3 perenggan ringkas**
- Sertakan contoh atau analogi jika perlu untuk memudahkan pemahaman

✅ Output WAJIB ditulis dalam **Bahasa Melayu** sepenuhnya.

✅ Format output WAJIB seperti ini:

🎓 **Sesi Belajar Trading Hari Ini**
📚 *{current_topic['title']}*

[Perenggan 1: Terangkan konsep atau masalah berkaitan {current_topic['title']}. Terus kepada point utama.]

[Perenggan 2: Berikan solusi, penjelasan, atau tips praktikal berkaitan {current_topic['focus']}. Gunakan point form jika perlu.]

[Perenggan 3: Kesimpulan ringkas atau kata-kata semangat.]

Akhiri dengan **1–2 emoji** dan **hashtag**:
`#BelajarTrading #TipsForex #SahamMalaysia #CryptoEducation #TraderMindset`

Contoh gaya (Untuk topik Risk Management):
🎓 **Sesi Belajar Trading Hari Ini**
📚 *Seni Pengurusan Risiko*

Ramai trader baru anggap Stop Loss (SL) sebagai musuh. Sebenarnya, SL adalah 'insurans' anda. Tanpa SL, satu pergerakan pasaran yang drastik boleh hanguskan akaun. 📉

Bayangkan memandu tanpa brek. Anda mungkin laju, tapi bila ada halangan, anda tak boleh berhenti. Begitu juga trading. SL membolehkan anda 'berhenti' rugi sebelum parah. Itu adalah risk management bijak. 🛡️

Jadi, jangan takut kena SL. Takutlah kalau tak ada SL langsung. Jaga modal, profit akan datang kemudian. 💪
#TipsForex #TraderMindset

Tugas anda hari ini adalah hasilkan **1 tips pendidikan unik berdasarkan topik dan fokus hari ini**, berformat seperti di atas, dalam Bahasa Melayu.
"""

# Generate education tip using OpenAI
def generate_education_tip():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if accessible
        messages=[
            {"role": "system", "content": "Anda adalah mentor dagangan yang bijak dan suka berkongsi ilmu."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# Send to Telegram
async def main():
    if not GROUP_CHAT_ID_EDUCATION:
        print("⚠️ Warning: GROUP_CHAT_ID_EDUCATION is not set in .env file.")
        # Optional: Fallback to FUN ID if you want, but better to warn.
        # chat_id = os.getenv("GROUP_CHAT_ID_FUN") 
        return

    tip = generate_education_tip()
    await bot.send_message(chat_id=GROUP_CHAT_ID_EDUCATION, text=tip, parse_mode='Markdown')

# Run
if __name__ == "__main__":
    asyncio.run(main())
