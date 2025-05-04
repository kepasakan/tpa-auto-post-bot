import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from telegram import Bot

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Prepare Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Prompt to generate a trading-related fun fact
prompt = """
Bertindak sebagai seorang guru dagangan yang menyeronokkan. Tugas anda adalah untuk memberikan *1 fakta menarik atau pelik berkaitan dunia dagangan (forex, saham, crypto atau indeks)* yang:

- Mengejutkan atau tidak biasa
- Benar & relevan untuk trader
- Ringkas (1 perenggan)
- Gaya bahasa santai tetapi berinformasi
- Sesuai untuk dihantar ke saluran Telegram

Sertakan emoji dan tarik minat pembaca. Jangan terlalu panjang.
"""

# Generate content
response = model.generate_content(prompt)
fact = response.text.strip()

# Format for Telegram
today = datetime.now().strftime('%d/%m/%Y')
message = f"🎉 *Fun Fact Dagangan Hari Ini* ({today})\n\n{fact}"

# Send to Telegram
bot = Bot(token=BOT_TOKEN)
bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode='Markdown')

