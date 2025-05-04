import os
import google.generativeai as genai
from datetime import datetime

# Load local .env only if not running in GitHub Actions
if not os.getenv("GITHUB_ACTIONS"):
    from dotenv import load_dotenv
    load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Format today's date (e.g., 4 Mei 2025)
today = datetime.now().strftime('%#d %B %Y') # Malay-style format

# Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Prompt with today's date
prompt = f"""
Bertindak sebagai seorang penganalisis pasaran profesional dan jurulatih dagangan yang pakar dalam menyampaikan sentimen pasaran harian untuk pedagang forex, komoditi, dan indeks.

Hari ini adalah: **{today}**

Sediakan **Ringkasan Pasaran Harian** yang komprehensif, praktikal, dan sesuai untuk trader prop firm.  
Analisis ini mesti berdasarkan:
- Data ekonomi semasa (NFP, CPI, PMI, kadar faedah, dll.)
- Berita berimpak tinggi & kenyataan rasmi bank pusat (FOMC, ECB, BOE, dll.)
- **Isu geopolitik & fundamental global terkini** (contoh: pilihan raya AS, tindakan Trump, China, konflik Timur Tengah)
- Reaksi pasaran semasa terhadap faktor-faktor ini

Fokuskan kepada:
- **Pasangan mata wang utama**: USD, EUR, GBP, JPY, AUD, NZD, CAD, CHF  
- **Komoditi penting**: Emas (XAUUSD), Minyak Mentah (WTI)  
- **Indeks utama**: Nasdaq (NAS100), S&P500 (SPX500)  

**Tugas anda:**
- Jangan hanya nyatakan arah (bullish/bearish), berikan **penjelasan ringkas** untuk setiap pergerakan pasaran (kenapa ia berlaku).  
- Gunakan bahasa **yang jelas, padat, dan sedia untuk dipos ke saluran Telegram.**

Jawapan mesti mengandungi:

1. **🔥 Poin Utama (gaya headline)** — ringkasan utama yang trader perlu tahu hari ini  
2. **🌍 Sentimen Pasaran** — overview sentimen global (bullish, bearish, berhati-hati) dengan sedikit konteks  
3. **📊 Sorotan Mata Wang & Komoditi**  
   - Untuk setiap aset (USD, EUR, GBP, dll. + XAUUSD, WTI, NAS100, SPX500), nyatakan arah (bullish/bercampur/bearish) **dan penjelasan ringkas 1 ayat kenapa**  
4. **💬 Tip Psikologi Hari Ini** — nasihat mindset/risk/disiplin  
5. **🕒 Waktu Dagangan Ideal (MYT)** — waktu terbaik untuk peluang/volatiliti  

**Contoh format jawapan akhir (wajib ikut):**

🔥 Poin Utama:  
🌍 Sentimen Pasaran:  
📊 Sorotan Mata Wang & Komoditi:  
- **USD:** Bullish – Data NFP menguat & Fed mungkin kekal hawkish  
- **XAUUSD (Emas):** Bearish – USD menguat dan tiada risk-off besar  
- **NAS100:** Berhati-hati – Isu pilihan raya AS & retorik Trump menyebabkan ketidaktentuan  
💬 Tip Psikologi Hari Ini:  
🕒 Waktu Dagangan Ideal (MYT):  

"""

response = model.generate_content(prompt)

# Output
print(f"\n📊 Market Insight - {today}")
print(response.text)
