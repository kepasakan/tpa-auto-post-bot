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

# Get today's date
today = datetime.now().strftime('%d/%m/%Y')

# Prompt for education tip
prompt = f"""
Bertindak sebagai seorang mentor dagangan yang berpengalaman, bijak, dan sangat membantu. Tugas anda adalah untuk menghasilkan *1 tips pendidikan, panduan, atau nasihat dagangan* yang bernilai tinggi berkaitan dunia dagangan seperti forex, saham, kripto, atau indeks.

Hari ini ialah: **{today}**

✅ Tips mesti:
- Berdasarkan prinsip dagangan yang betul (teknikal, fundamental, atau psikologi)
- Memberikan nilai tambah kepada trader (beginner atau intermediate)
- *Bukan signal buy/sell*, tetapi ilmu atau nasihat
- Ditulis dalam gaya bahasa profesional tetapi mudah difahami (santai)
- Disampaikan dalam **2-3 perenggan ringkas**
- Sertakan contoh atau analogi jika perlu untuk memudahkan pemahaman

✅ Output WAJIB ditulis dalam **Bahasa Melayu** sepenuhnya.

✅ Format output WAJIB seperti ini:

🎓 **Sesi Belajar Trading Hari Ini**
📚 *[Tajuk Topik/Tips di sini]*

[Perenggan 1: Terangkan konsep atau masalah yang sering dihadapi trader. Terus kepada point utama.]

[Perenggan 2: Berikan solusi, penjelasan teknik, atau cara mengatasi masalah tersebut. Gunakan point form jika perlu untuk kejelasan.]

[Perenggan 3: Kesimpulan ringkas atau kata-kata semangat untuk trader terus belajar.]

Akhiri dengan **1–2 emoji** dan **hashtag**:
`#BelajarTrading #TipsForex #SahamMalaysia #CryptoEducation #TraderMindset`

Contoh gaya:
🎓 **Sesi Belajar Trading Hari Ini**
📚 *Kenapa Stop Loss Itu Penting?*

Ramai trader baru anggap Stop Loss (SL) sebagai musuh yang buat akaun rugi. Sebenarnya, SL adalah 'insurans' anda. Tanpa SL, satu pergerakan pasaran yang drastik boleh hanguskan keseluruhan modal anda dalam sekelip mata. 📉

Bayangkan memandu kereta tanpa brek. Anda mungkin laju, tapi bila ada halangan, anda tak boleh berhenti. Begitu juga trading. SL membolehkan anda 'berhenti' rugi sebelum ia menjadi parah. Ia adalah sebahagian daripada pengurusan risiko yang bijak. 🛡️

Jadi, jangan takut kena SL. Takutlah kalau tak ada SL langsung. Jaga modal, profit akan datang kemudian. 💪
#TipsForex #TraderMindset

Tugas anda hari ini adalah hasilkan **1 tips pendidikan unik dan berformat seperti di atas**, dalam Bahasa Melayu.
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
