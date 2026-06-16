# 🚀 TODO DETAIL - BOT TELEGRAM SISKAPERBAPO
## Panduan Implementasi Step-by-Step

> **CATATAN:** Setiap fase memiliki checklist detail. Tandai dengan ✅ setelah selesai.
> Jangan lompat ke fase berikutnya sebelum fase sekarang benar-benar selesai dan tested.

---

## 📑 DAFTAR ISI
- [Fase 0: Setup Project & Architecture](#fase-0-setup-project--architecture)
- [Fase 1: Persiapan & Setup Dasar](#fase-1-persiapan--setup-dasar)
- [Fase 2: Ekstraksi & Pengolahan Data](#fase-2-ekstraksi--pengolahan-data)
- [Fase 3: Integrasi Bot & Database](#fase-3-integrasi-bot--database)
- [Fase 4: Otomatisasi & Scheduling](#fase-4-otomatisasi--scheduling)
- [Fase 5: Testing & Quality Assurance](#fase-5-testing--quality-assurance)
- [Fase 6: Deployment](#fase-6-deployment)
- [Fase 7: Monitoring & Maintenance](#fase-7-monitoring--maintenance)

---

## ✅ STATUS IMPLEMENTASI TERKINI

Update terakhir: fondasi MVP awal sudah selesai, scraper AJAX Siskaperbapo sudah diperbaiki, dan project sudah dipush ke GitHub.

### Sudah selesai
- [x] Struktur project Python dibuat.
- [x] `.gitignore`, `.env.example`, `requirements.txt`, `setup.cfg`, dan `README.md` dibuat.
- [x] Dependency diinstall dan disesuaikan untuk Python 3.13.
- [x] Dependency `html5lib` ditambahkan untuk fallback parsing HTML.
- [x] Config environment dibuat di `config/settings.py`.
- [x] Constants daerah dan pesan bot dibuat di `config/constants.py`.
- [x] Logger dengan rotating file handler dibuat.
- [x] Entry point bot dibuat di `main.py`.
- [x] Handler bot dibuat untuk `/start`, `/help`, `/daerah`, `/cek`, dan `/stop`.
- [x] Inline keyboard pilihan daerah dibuat.
- [x] Database SQLite dibuat dengan tabel `users`.
- [x] CRUD dasar user/subscription dibuat.
- [x] Scraper Siskaperbapo awal dibuat.
- [x] Scraper diperbaiki agar memakai endpoint AJAX `tabel.nodesign`.
- [x] Parser tabel HTML dibuat.
- [x] Parser diperbaiki agar harga `15.900` tidak berubah menjadi `15.9`.
- [x] Formatter pesan Telegram dibuat.
- [x] Message splitting untuk pesan panjang dibuat.
- [x] Unit test dasar dibuat untuk URL builder, parser, dan formatter.
- [x] Unit test parser struktur tabel AJAX Siskaperbapo ditambahkan.
- [x] `python -m compileall .` berhasil.
- [x] `python -m pytest tests` berhasil: 6 test passed.
- [x] `python -m black --check .` berhasil.
- [x] `python -m flake8 .` berhasil.
- [x] Diagnostics project bersih tanpa error/warning.
- [x] Commit lokal dibuat.
- [x] Remote GitHub dipasang: `https://github.com/rab781/BakoBot.git`.
- [x] Project berhasil dipush ke branch `main`.

### Belum selesai / berikutnya
- [ ] Buat file `.env` lokal dan isi `TELEGRAM_BOT_TOKEN` asli.
- [x] Test manual awal bot langsung di Telegram: `/start`, pilih daerah, dan `/cek` berjalan sampai scraping.
- [ ] Test manual ulang `/cek` setelah fix scraper AJAX.
- [x] Validasi scraping nyata untuk `jemberkab` berhasil: 67 record.
- [ ] Validasi scraping nyata untuk beberapa daerah lain di Siskaperbapo.
- [ ] Implementasi scheduler broadcast harian dengan APScheduler.
- [ ] Tambahkan rate limiting per user.
- [ ] Tambahkan backup database otomatis.
- [ ] Tambahkan notifikasi error ke admin.
- [ ] Siapkan deployment 24/7.

---

# FASE 0: Setup Project & Architecture
**Estimasi Waktu:** 2-3 jam  
**Tujuan:** Setup struktur project yang proper dan scalable

## 0.1. Inisialisasi Git Repository
- [x] Jalankan `git init` di folder project
- [x] Create repository di GitHub/GitLab
- [x] Connect local dengan remote: `git remote add origin <URL>`

Catatan selesai:
- Remote GitHub: `https://github.com/rab781/BakoBot.git`
- Branch aktif: `main`
- Project sudah dipush ke GitHub.

## 0.2. Buat Struktur Folder
Buat folder structure berikut:

```bash
mkdir -p src/bot src/scraper src/database src/utils config tests logs backups data
```

- [x] Buat folder `src/` - Source code utama
- [x] Buat folder `src/bot/` - Telegram bot handlers
- [x] Buat folder `src/scraper/` - Web scraping logic
- [x] Buat folder `src/database/` - Database operations
- [x] Buat folder `src/utils/` - Helper functions
- [x] Buat folder `config/` - Configuration files
- [x] Buat folder `tests/` - Unit & integration tests
- [x] Buat folder `logs/` - Log files (add to .gitignore)
- [x] Buat folder `backups/` - Database backups (add to .gitignore)
- [x] Buat folder `data/` - SQLite database (add to .gitignore)

## 0.3. Buat File __init__.py
Buat file `__init__.py` di setiap folder Python:

- [x] `src/__init__.py`
- [x] `src/bot/__init__.py`
- [x] `src/scraper/__init__.py`
- [x] `src/database/__init__.py`
- [x] `src/utils/__init__.py`
- [x] `config/__init__.py`

## 0.4. Setup .gitignore
- [x] Buat file `.gitignore`

**Isi file `.gitignore`:**
```gitignore
# Environment Variables
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Database
*.db
*.sqlite
*.sqlite3
data/

# Logs
logs/
*.log

# Backups
backups/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
```

## 0.5. Setup Environment Variables
- [ ] Buat file `.env` (untuk development local)
- [x] Buat file `.env.example` (template tanpa sensitive data, di-commit ke git)

**File `.env.example`:**
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
ADMIN_CHAT_ID=your_admin_chat_id_here

# Database Configuration
DATABASE_PATH=data/botbako.db

# Scraping Configuration
SISKAPERBAPO_BASE_URL=https://siskaperbapo.jatimprov.go.id/harga/tabel/
SCRAPING_TIMEOUT=30
SCRAPING_RETRY_ATTEMPTS=3

# Scheduler Configuration
BROADCAST_TIME=08:00
TIMEZONE=Asia/Jakarta

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log

# Rate Limiting
USER_COMMAND_RATE_LIMIT=5
USER_COMMAND_RATE_PERIOD=60
```

**File `.env` (copy dari .env.example dan isi dengan nilai real):**
- [ ] Copy `.env.example` ke `.env`
- [ ] Isi `TELEGRAM_BOT_TOKEN` dengan token dari BotFather
- [ ] Isi `ADMIN_CHAT_ID` dengan chat ID Telegram kamu

## 0.6. Setup Requirements
- [x] Buat file `requirements.txt`

**Isi file `requirements.txt`:**
```txt
# Telegram Bot
python-telegram-bot==20.7

# Web Scraping
requests==2.31.0
pandas==2.1.4
lxml==4.9.3
beautifulsoup4==4.12.2

# Database
sqlalchemy==2.0.23

# Scheduling
APScheduler==3.10.4
pytz==2023.3

# Configuration
python-dotenv==1.0.0

# Retry & Error Handling
tenacity==8.2.3

# Logging
colorlog==6.8.0

# Testing (dev dependencies)
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
faker==20.1.0

# Code Quality (dev dependencies)
black==23.12.1
flake8==6.1.0
mypy==1.7.1
```

- [x] Install dependencies: `pip install -r requirements.txt`

## 0.7. Setup Virtual Environment
- [ ] Buat virtual environment: `python -m venv venv`
- [ ] Activate venv:
  - Windows: `venv\Scripts\activate`
  - Linux/Mac: `source venv/bin/activate`
- [ ] Install requirements: `pip install -r requirements.txt`

**✅ CHECKLIST FASE 0:**
- [x] Git repository initialized
- [x] Folder structure created
- [x] .gitignore configured
- [ ] .env dibuat dan diisi token asli
- [x] .env.example created
- [x] requirements.txt created
- [x] Dependencies installed
- [x] Commit semua ke git
- [x] Push ke GitHub

---

# FASE 1: Persiapan & Setup Dasar
**Estimasi Waktu:** 2-3 jam  
**Tujuan:** Setup Telegram Bot dasar dan configuration system

## 1.1. Setup BotFather (Telegram)
- [ ] Buka Telegram, cari `@BotFather`
- [ ] Kirim `/newbot`
- [ ] Atur nama bot (misal: "Siskaperbapo Bot")
- [ ] Atur username bot (misal: "siskaperbapo_jatim_bot")
- [ ] **SIMPAN TOKEN yang diberikan ke file `.env`**
- [ ] Set deskripsi bot: `/setdescription`
- [ ] Set about text: `/setabouttext`
- [ ] (Optional) Upload foto bot: `/setuserpic`

**Cara mendapatkan ADMIN_CHAT_ID:**
- [ ] Kirim pesan ke bot `@userinfobot` di Telegram
- [ ] Copy chat ID kamu
- [ ] Paste ke `.env` di variable `ADMIN_CHAT_ID`

## 1.2. Buat Configuration Module
**File: `config/settings.py`**

- [x] Buat file `config/settings.py`
- [x] Implement configuration loader

**Code untuk `config/settings.py`:**
```python
"""Configuration management using environment variables."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file!")

# Database Configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/botbako.db')
DATABASE_FULL_PATH = PROJECT_ROOT / DATABASE_PATH

# Scraping Configuration
SISKAPERBAPO_BASE_URL = os.getenv(
    'SISKAPERBAPO_BASE_URL',
    'https://siskaperbapo.jatimprov.go.id/harga/tabel/'
)
SCRAPING_TIMEOUT = int(os.getenv('SCRAPING_TIMEOUT', '30'))
SCRAPING_RETRY_ATTEMPTS = int(os.getenv('SCRAPING_RETRY_ATTEMPTS', '3'))

# Scheduler Configuration
BROADCAST_TIME = os.getenv('BROADCAST_TIME', '08:00')
TIMEZONE = os.getenv('TIMEZONE', 'Asia/Jakarta')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = PROJECT_ROOT / os.getenv('LOG_FILE', 'logs/bot.log')

# Rate Limiting
USER_COMMAND_RATE_LIMIT = int(os.getenv('USER_COMMAND_RATE_LIMIT', '5'))
USER_COMMAND_RATE_PERIOD = int(os.getenv('USER_COMMAND_RATE_PERIOD', '60'))
```

- [ ] Test import: `python -c "from config.settings import TELEGRAM_BOT_TOKEN; print('OK')`

## 1.3. Buat Constants Module
**File: `config/constants.py`**

- [x] Buat file `config/constants.py`
- [x] Define semua constants (daerah, messages, emojis)

**Code untuk `config/constants.py`:**
```python
"""Constants and static data."""

# Daftar Kabupaten/Kota di Jawa Timur dengan kode
DAERAH_LIST = {
    'surabayakota': 'Kota Surabaya',
    'malangkota': 'Kota Malang',
    'madiunkota': 'Kota Madiun',
    'kediri': 'Kota Kediri',
    'blitar': 'Kota Blitar',
    'mojokertokota': 'Kota Mojokerto',
    'pasuruan': 'Kota Pasuruan',
    'probolinggokota': 'Kota Probolinggo',
    'batukota': 'Kota Batu',
    
    'bangkalankab': 'Kab. Bangkalan',
    'banyuwangikab': 'Kab. Banyuwangi',
    'blitarkab': 'Kab. Blitar',
    'bojonegorokab': 'Kab. Bojonegoro',
    'bondowosokab': 'Kab. Bondowoso',
    'gresikkab': 'Kab. Gresik',
    'jemberkab': 'Kab. Jember',
    'jombangkab': 'Kab. Jombang',
    'kedirikab': 'Kab. Kediri',
    'lamongankab': 'Kab. Lamongan',
    'lumajangkab': 'Kab. Lumajang',
    'madiunkab': 'Kab. Madiun',
    'magetankab': 'Kab. Magetan',
    'malangkab': 'Kab. Malang',
    'mojokertokab': 'Kab. Mojokerto',
    'nganjukkab': 'Kab. Nganjuk',
    'ngawikab': 'Kab. Ngawi',
    'pacitkankab': 'Kab. Pacitan',
    'pamuekasankab': 'Kab. Pamekasan',
    'pasuruankab': 'Kab. Pasuruan',
    'ponorogokab': 'Kab. Ponorogo',
    'probolinggokab': 'Kab. Probolinggo',
    'sampangkab': 'Kab. Sampang',
    'sidoarjokab': 'Kab. Sidoarjo',
    'situbondokab': 'Kab. Situbondo',
    'sumenepkab': 'Kab. Sumenep',
    'trenggalekkab': 'Kab. Trenggalek',
    'tubankab': 'Kab. Tuban',
    'tulungagungkab': 'Kab. Tulungagung',
}

# Bot Messages
MESSAGES = {
    'welcome': """
🌾 *Selamat datang di Bot Harga Komoditas Siskaperbapo Jawa Timur!*

Bot ini akan memberikan update harga komoditas pangan di daerah Anda setiap hari.

📍 Silakan pilih daerah Anda terlebih dahulu.

Gunakan /help untuk melihat perintah yang tersedia.
""",
    
    'help': """
📖 *PANDUAN PENGGUNAAN BOT*

🔹 /start - Mulai menggunakan bot dan pilih daerah
🔹 /cek - Cek harga komoditas saat ini
🔹 /daerah - Ganti pilihan daerah
🔹 /stop - Berhenti menerima update otomatis
🔹 /help - Tampilkan panduan ini

💡 Bot akan mengirim update harga otomatis setiap hari pukul 08:00 WIB.
""",
    
    'choose_region': "📍 Silakan pilih daerah Anda:",
    
    'region_saved': """
✅ *Daerah tersimpan: {daerah}*

Anda akan menerima update harga komoditas untuk daerah ini setiap hari pukul 08:00 WIB.

Gunakan /cek untuk melihat harga sekarang.
""",
    
    'loading': "⏳ Mengambil data harga komoditas...",
    
    'data_unavailable': """
❌ *Data tidak tersedia*

Maaf, data harga untuk daerah Anda sedang tidak tersedia.
Silakan coba lagi nanti.
""",
    
    'error_occurred': """
⚠️ *Terjadi kesalahan*

Maaf, terjadi kesalahan saat memproses permintaan Anda.
Tim kami sudah diberitahu dan akan segera memperbaikinya.
""",
    
    'unsubscribed': """
✅ *Berhenti berlangganan*

Anda tidak akan menerima update otomatis lagi.
Gunakan /start kapan saja untuk berlangganan kembali.
""",
    
    'no_region_set': """
❌ *Belum memilih daerah*

Silakan gunakan /start untuk memilih daerah terlebih dahulu.
""",
    
    'rate_limit': """
⏱️ *Terlalu banyak permintaan*

Mohon tunggu sebentar sebelum mengirim perintah lagi.
""",
}

# Emojis
EMOJI = {
    'beras': '🌾',
    'gula': '🍬',
    'minyak': '🛢️',
    'telur': '🥚',
    'ayam': '🐔',
    'daging': '🥩',
    'cabai': '🌶️',
    'bawang': '🧅',
    'tomat': '🍅',
    'default': '📦',
}

# Komoditas keywords untuk emoji mapping
KOMODITAS_EMOJI_MAP = {
    'beras': '🌾',
    'gula': '🍬',
    'minyak': '🛢️',
    'telur': '🥚',
    'ayam': '🐔',
    'daging': '🥩',
    'sapi': '🥩',
    'cabai': '🌶️',
    'cabe': '🌶️',
    'bawang': '🧅',
    'tomat': '🍅',
    'merah': '🔴',
    'putih': '⚪',
}
```

## 1.4. Setup Logging System
**File: `src/utils/logger.py`**

- [x] Buat file `src/utils/logger.py`
- [x] Implement proper logging dengan rotation

**Code untuk `src/utils/logger.py`:**
```python
"""Logging configuration with rotation and formatting."""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

from config.settings import LOG_FILE, LOG_LEVEL

def setup_logger(name: str = 'botbako') -> logging.Logger:
    """
    Setup logger with console and file handlers.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create logs directory if not exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File Handler with Rotation (10MB max, keep 5 backups)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Create default logger
logger = setup_logger()
```

- [ ] Test logging: 
```python
from src.utils.logger import logger
logger.info("Logging test OK")
```

## 1.5. Buat Bot Sederhana (Ping Pong)
**File: `main.py`**

- [x] Buat file `main.py` di root folder
- [x] Implement basic bot yang respond `/start`
- [x] Register command `/help`, `/daerah`, `/cek`, dan `/stop`
- [x] Register callback handler untuk pilihan daerah

**Code untuk `main.py` (versi basic):**
```python
"""Main entry point for the bot."""
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config.settings import TELEGRAM_BOT_TOKEN
from src.utils.logger import logger

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text(
        "🌾 Bot Siskaperbapo aktif!\n\n"
        "Ini adalah test version. Stay tuned!"
    )
    logger.info(f"User {update.effective_user.id} started the bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    await update.message.reply_text(
        "📖 Perintah yang tersedia:\n"
        "/start - Mulai bot\n"
        "/help - Bantuan"
    )

def main():
    """Start the bot."""
    logger.info("Starting bot...")
    
    # Create application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # Start bot
    logger.info("Bot is running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
```

- [ ] **TEST: Jalankan bot** `python main.py`
- [ ] **TEST: Buka Telegram, cari bot kamu, kirim `/start`**
- [ ] **TEST: Bot harus reply dengan pesan test**
- [ ] **TEST: Check logs di folder `logs/`**

**✅ CHECKLIST FASE 1:**
- [ ] BotFather setup selesai
- [ ] Token tersimpan di .env
- [x] config/settings.py created & tested
- [x] config/constants.py created
- [x] src/utils/logger.py created & tested
- [x] main.py created
- [ ] Bot bisa respond ke /start dan /help setelah `.env` diisi token asli
- [x] Logging berfungsi dengan baik
- [x] Commit dan push sudah dilakukan

---

# FASE 2: Ekstraksi & Pengolahan Data
**Estimasi Waktu:** 4-5 jam  
**Tujuan:** Build web scraper yang robust dengan error handling

## 2.1. Buat URL Builder
**File: `src/scraper/url_builder.py`**

- [ ] Buat file `src/scraper/url_builder.py`
- [ ] Implement fungsi untuk build URL dinamis

**Code untuk `src/scraper/url_builder.py`:**
```python
"""URL builder for Siskaperbapo website."""
from datetime import date, datetime
from typing import Optional

from config.settings import SISKAPERBAPO_BASE_URL
from src.utils.logger import logger

def build_url(kode_daerah: str, tanggal: Optional[date] = None) -> str:
    """
    Build URL for Siskaperbapo data.
    
    Args:
        kode_daerah: Region code (e.g., 'surabayakota')
        tanggal: Date to fetch. If None, use today.
        
    Returns:
        Full URL string
        
    Example:
        >>> build_url('bondowosokab', date(2024, 1, 15))
        'https://siskaperbapo.jatimprov.go.id/harga/tabel/?kabkota=bondowosokab&tanggal=2024-01-15'
    """
    if tanggal is None:
        tanggal = date.today()
    
    tanggal_str = tanggal.strftime('%Y-%m-%d')
    url = f"{SISKAPERBAPO_BASE_URL}?kabkota={kode_daerah}&tanggal={tanggal_str}"
    
    logger.debug(f"Built URL: {url}")
    return url
```

- [ ] Test: `python -c "from src.scraper.url_builder import build_url; print(build_url('surabayakota'))"`

## 2.2. Buat HTTP Client dengan Retry
**File: `src/scraper/http_client.py`**

- [ ] Buat file `src/scraper/http_client.py`
- [ ] Implement HTTP client dengan retry mechanism

**Code untuk `src/scraper/http_client.py`:**
```python
"""HTTP client with retry mechanism."""
import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from typing import Optional

from config.settings import SCRAPING_TIMEOUT, SCRAPING_RETRY_ATTEMPTS
from src.utils.logger import logger

class ScrapingError(Exception):
    """Custom exception for scraping errors."""
    pass

@retry(
    stop=stop_after_attempt(SCRAPING_RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((requests.RequestException, requests.Timeout)),
    reraise=True
)
def fetch_url(url: str) -> str:
    """
    Fetch URL with retry mechanism.
    
    Args:
        url: URL to fetch
        
    Returns:
        HTML content as string
        
    Raises:
        ScrapingError: If fetching fails after retries
    """
    logger.info(f"Fetching URL: {url}")
    
    try:
        response = requests.get(
            url,
            timeout=SCRAPING_TIMEOUT,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        response.raise_for_status()
        
        logger.info(f"Successfully fetched URL (status {response.status_code})")
        return response.text
        
    except requests.Timeout as e:
        logger.error(f"Timeout fetching URL: {url}")
        raise ScrapingError(f"Timeout: {e}")
        
    except requests.RequestException as e:
        logger.error(f"Error fetching URL: {e}")
        raise ScrapingError(f"Request error: {e}")
```

## 2.3. Buat Data Parser
**File: `src/scraper/parser.py`**

- [ ] Buat file `src/scraper/parser.py`
- [ ] Implement parsing dan cleaning data

**Code untuk `src/scraper/parser.py`:**
```python
"""HTML parser and data cleaner."""
import pandas as pd
from typing import Optional, Dict, List
from io import StringIO

from src.utils.logger import logger

def parse_html_table(html: str) -> Optional[pd.DataFrame]:
    """
    Parse HTML table using pandas.
    
    Args:
        html: HTML content as string
        
    Returns:
        DataFrame or None if parsing failed
    """
    try:
        # Try to read all tables in HTML
        tables = pd.read_html(StringIO(html))
        
        if not tables:
            logger.warning("No tables found in HTML")
            return None
        
        # Assume first table is the data we need
        df = tables[0]
        logger.info(f"Parsed table with shape {df.shape}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error parsing HTML table: {e}")
        return None

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate DataFrame.
    
    Args:
        df: Raw DataFrame from parsing
        
    Returns:
        Cleaned DataFrame
    """
    # Remove empty rows
    df = df.dropna(how='all')
    
    # Remove empty columns
    df = df.dropna(axis=1, how='all')
    
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    
    # Remove rows where all values are '-' or 'nan'
    df = df[~df.isin(['-', 'nan', '']).all(axis=1)]
    
    logger.info(f"Cleaned DataFrame shape: {df.shape}")
    return df

def dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, str]]:
    """
    Convert DataFrame to list of dictionaries.
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        List of dictionaries
    """
    # Expected columns (adjust based on actual website structure)
    # Example: ['No', 'Komoditas', 'Satuan', 'Harga']
    
    result = []
    
    for _, row in df.iterrows():
        try:
            # Adjust this based on actual table structure
            item = {
                'komoditas': str(row.iloc[1]) if len(row) > 1 else 'N/A',
                'satuan': str(row.iloc[2]) if len(row) > 2 else 'N/A',
                'harga': str(row.iloc[3]) if len(row) > 3 else 'N/A',
            }
            result.append(item)
        except Exception as e:
            logger.warning(f"Error parsing row: {e}")
            continue
    
    return result
```

## 2.4. Buat Main Scraper
**File: `src/scraper/siskaperbapo.py`**

- [ ] Buat file `src/scraper/siskaperbapo.py`
- [ ] Integrate semua komponen scraper

**Code untuk `src/scraper/siskaperbapo.py`:**
```python
"""Main scraper for Siskaperbapo website."""
from datetime import date
from typing import Optional, List, Dict

from src.scraper.url_builder import build_url
from src.scraper.http_client import fetch_url, ScrapingError
from src.scraper.parser import parse_html_table, clean_dataframe, dataframe_to_dict
from src.utils.logger import logger

def scrape_harga(kode_daerah: str, tanggal: Optional[date] = None) -> Optional[List[Dict[str, str]]]:
    """
    Scrape harga komoditas from Siskaperbapo.
    
    Args:
        kode_daerah: Region code
        tanggal: Date to scrape. If None, use today.
        
    Returns:
        List of dictionaries with commodity data, or None if failed
        
    Example:
        >>> data = scrape_harga('surabayakota')
        >>> print(data[0])
        {'komoditas': 'Beras Premium', 'satuan': 'Kg', 'harga': '12000'}
    """
    try:
        # Build URL
        url = build_url(kode_daerah, tanggal)
        
        # Fetch HTML
        html = fetch_url(url)
        
        # Parse table
        df = parse_html_table(html)
        if df is None or df.empty:
            logger.warning(f"No data found for {kode_daerah}")
            return None
        
        # Clean data
        df = clean_dataframe(df)
        
        # Convert to dict
        data = dataframe_to_dict(df)
        
        if not data:
            logger.warning(f"No valid data after cleaning for {kode_daerah}")
            return None
        
        logger.info(f"Successfully scraped {len(data)} items for {kode_daerah}")
        return data
        
    except ScrapingError as e:
        logger.error(f"Scraping error for {kode_daerah}: {e}")
        return None
        
    except Exception as e:
        logger.exception(f"Unexpected error scraping {kode_daerah}: {e}")
        return None
```

## 2.5. Buat Formatter Pesan
**File: `src/utils/formatters.py`**

- [ ] Buat file `src/utils/formatters.py`
- [ ] Format hasil scraping menjadi pesan Telegram yang rapi

**Tujuan formatter:**
- Membuat header tanggal dan nama daerah
- Mengubah daftar komoditas menjadi format bullet
- Menambahkan emoji sesuai jenis komoditas
- Membatasi panjang pesan agar tidak melebihi limit Telegram

**Checklist implementasi:**
- [ ] Buat fungsi `get_emoji_for_commodity(nama_komoditas)`
- [ ] Buat fungsi `format_harga_message(daerah, data, tanggal)`
- [ ] Buat fungsi `split_long_message(message, max_length=4000)`
- [ ] Pastikan harga dan satuan tampil konsisten
- [ ] Pastikan jika data kosong, formatter mengembalikan pesan fallback

## 2.6. Validasi Hasil Scraping
- [ ] Test scraping untuk minimal 3 daerah berbeda
- [ ] Test untuk tanggal hari ini
- [ ] Test untuk tanggal yang kemungkinan tidak ada data
- [ ] Cek apakah struktur kolom hasil scraping konsisten
- [ ] Verifikasi apakah `komoditas`, `satuan`, dan `harga` benar posisinya
- [ ] Simpan contoh output mentah untuk debugging

## 2.7. Tambahkan Fallback & Catatan Risiko
- [ ] Jika parsing tabel gagal, log HTML atau potongan response untuk investigasi
- [ ] Jika website lambat, tampilkan timeout yang user-friendly
- [ ] Jika website berubah struktur, siapkan parser cadangan
- [ ] Jika data kosong, jangan anggap bot rusak — beri pesan bahwa data belum tersedia

**✅ CHECKLIST FASE 2:**
- [x] URL builder selesai
- [x] HTTP client dengan timeout dan retry selesai
- [x] Parser HTML selesai
- [x] Cleaning dataframe selesai
- [x] Main scraper selesai
- [x] Formatter pesan selesai
- [ ] Scraper berhasil dites manual untuk beberapa daerah real
- [x] Error handling dasar scraping sudah ada
- [x] Unit test parser/formatter/URL builder tersedia
- [x] Commit dan push sudah dilakukan

---

# FASE 3: Integrasi Bot & Database
**Estimasi Waktu:** 4-6 jam  
**Tujuan:** Menghubungkan bot Telegram dengan data user dan hasil scraping

## 3.1. Tentukan Skema Database
**Rekomendasi awal:** gunakan SQLite

**Data minimal yang perlu disimpan:**
- `chat_id`
- `username`
- `full_name`
- `kode_daerah`
- `is_subscribed`
- `created_at`
- `updated_at`

- [ ] Buat file `src/database/connection.py` terpisah jika database makin kompleks
- [ ] Buat file `src/database/models.py` terpisah jika database makin kompleks
- [x] Buat file `src/database/operations.py`

## 3.2. Implement Database Connection
- [x] Buat helper koneksi SQLite
- [x] Pastikan folder `data/` dibuat otomatis jika belum ada
- [x] Aktifkan mode WAL jika menggunakan SQLite
- [x] Tambahkan fungsi init database saat aplikasi start

## 3.3. Buat Tabel User Subscription
- [x] Buat tabel `users`
- [x] Tambahkan unique constraint untuk `chat_id`
- [x] Tambahkan index jika diperlukan

**Operasi yang harus tersedia:**
- [x] `upsert_user_region(...)`
- [x] `get_user_by_chat_id(chat_id)`
- [x] `upsert_user_region(chat_id, kode_daerah)` untuk create/update daerah
- [x] `set_subscription_status(chat_id, status)`
- [x] `get_all_subscribed_users()`

## 3.4. Buat Inline Keyboard untuk Pilihan Daerah
**File: `src/bot/keyboards.py`**

- [x] Buat tombol inline per daerah
- [ ] Pisahkan tombol per halaman jika terlalu banyak
- [x] Gunakan callback data yang aman dan singkat
- [ ] Tambahkan tombol `Batal` atau `Kembali`

## 3.5. Buat Handlers Bot
**File: `src/bot/handlers.py`**

### Command yang harus dibuat:
- [x] `/start` → tampilkan welcome + pilihan daerah
- [x] `/help` → tampilkan panduan
- [x] `/cek` → ambil data harga berdasarkan daerah user
- [x] `/daerah` → ubah daerah pilihan user
- [x] `/stop` → berhenti berlangganan

### Callback handler:
- [x] Handler untuk pilihan daerah dari inline keyboard
- [x] Simpan pilihan daerah ke database
- [x] Kirim konfirmasi setelah daerah tersimpan

### Error handler:
- [x] Tangani error global di Telegram application
- [x] Log semua exception penting
- [ ] Kirim notifikasi error yang aman ke user/admin secara lebih lengkap

## 3.6. Alur User yang Harus Diuji
### Alur user baru:
- [ ] User kirim `/start`
- [ ] Bot tampilkan pilihan daerah
- [ ] User pilih daerah
- [ ] Bot simpan data user
- [ ] Bot kirim pesan sukses

### Alur user lama:
- [ ] User kirim `/cek`
- [ ] Bot ambil `kode_daerah` dari database
- [ ] Bot scrape data
- [ ] Bot kirim hasil format rapi

### Alur ubah preferensi:
- [ ] User kirim `/daerah`
- [ ] Bot tampilkan pilihan daerah lagi
- [ ] User pilih daerah baru
- [ ] Database diupdate

### Alur unsubscribe:
- [ ] User kirim `/stop`
- [ ] Status subscribe diubah jadi `false`
- [ ] Bot kirim konfirmasi berhenti

## 3.7. Tambahkan Validasi & UX yang Lebih Baik
- [ ] Jika user belum pilih daerah dan kirim `/cek`, arahkan ke `/start`
- [ ] Tampilkan pesan loading sebelum scraping
- [ ] Hapus atau edit pesan loading setelah hasil muncul
- [ ] Jika data kosong, tampilkan pesan ramah
- [ ] Jika callback data invalid, jangan crash

## 3.8. Pertimbangan Penting
- [ ] Jangan gunakan dictionary in-memory untuk production
- [ ] Hindari hardcode list daerah di banyak tempat
- [ ] Pisahkan teks pesan ke constants/messages
- [ ] Simpan log interaksi penting user

**✅ CHECKLIST FASE 3:**
- [x] Database koneksi dan init selesai
- [x] Tabel users selesai
- [x] CRUD user dasar selesai
- [x] Inline keyboard daerah selesai
- [x] Handler `/start`, `/help`, `/cek`, `/daerah`, `/stop` selesai
- [x] Callback handler selesai
- [x] Error handler dasar selesai
- [ ] Semua alur user utama berhasil diuji manual di Telegram
- [x] Commit dan push sudah dilakukan

---

# FASE 4: Otomatisasi & Scheduling
**Estimasi Waktu:** 3-4 jam  
**Tujuan:** Mengirim update harga otomatis setiap hari

## 4.1. Pilih Scheduler
**Rekomendasi:** `APScheduler`

- [ ] Setup scheduler terpisah dari handler bot
- [ ] Gunakan timezone `Asia/Jakarta`
- [ ] Pastikan job tidak double-run

## 4.2. Buat Fungsi Broadcast
**Kebutuhan fungsi broadcast:**
- [ ] Ambil semua user yang masih subscribe
- [ ] Kelompokkan berdasarkan `kode_daerah` untuk efisiensi
- [ ] Scrape sekali per daerah, bukan sekali per user
- [ ] Kirim hasil ke semua user pada daerah tersebut
- [ ] Log hasil sukses dan gagal

**Optimasi penting:**
- [ ] Jangan scrape 100 kali jika 100 user memilih daerah yang sama
- [ ] Gunakan cache hasil scrape per daerah saat broadcast berjalan

## 4.3. Tangani Rate Limit Telegram
- [ ] Tambahkan delay kecil antar pengiriman pesan
- [ ] Jika pesan panjang, split menjadi beberapa bagian
- [ ] Tangani error jika user block bot atau chat tidak ditemukan
- [ ] Jika user invalid, tandai untuk dibersihkan dari database

## 4.4. Jadwal Pengiriman
- [ ] Ambil jam broadcast dari `.env`
- [ ] Buat job harian, misalnya pukul `08:00 WIB`
- [ ] Pastikan scheduler start saat bot start
- [ ] Pastikan ada graceful shutdown

## 4.5. Tambahkan Job Tambahan
- [ ] Job backup database otomatis
- [ ] Job cleanup logs lama
- [ ] Job health report ke admin (optional)

## 4.6. Test Broadcast
- [ ] Test dengan 2-3 user dummy
- [ ] Test beberapa user dengan daerah yang sama
- [ ] Test jika satu user gagal dikirimi pesan
- [ ] Test jika scraping gagal untuk satu daerah
- [ ] Pastikan broadcast tetap lanjut untuk user lain

**✅ CHECKLIST FASE 4:**
- [ ] APScheduler terpasang dan aktif
- [ ] Fungsi broadcast selesai
- [ ] Optimasi scraping per daerah selesai
- [ ] Delay/rate limiting dasar selesai
- [ ] Jadwal harian selesai
- [ ] Backup job tambahan minimal direncanakan
- [ ] Broadcast manual dan otomatis berhasil diuji
- [ ] Commit: `git add . && git commit -m "Fase 4: Scheduler and broadcast complete"`

---

# FASE 5: Testing & Quality Assurance
**Estimasi Waktu:** 4-6 jam  
**Tujuan:** Memastikan bot stabil sebelum dipublikasikan

## 5.1. Unit Test
- [x] Test URL builder
- [x] Test parser HTML
- [x] Test dataframe cleaner lewat parser flow
- [x] Test formatter pesan
- [ ] Test database operations dasar

## 5.2. Integration Test
- [ ] Test scraping end-to-end
- [ ] Test alur `/start` sampai simpan daerah
- [ ] Test `/cek` dengan user valid
- [ ] Test `/cek` dengan user tanpa daerah
- [ ] Test `/stop`

## 5.3. Manual Test Scenarios
- [ ] User baru daftar
- [ ] User ganti daerah
- [ ] User berhenti langganan
- [ ] Website target tidak bisa diakses
- [ ] Data kosong
- [ ] Telegram API error sementara

## 5.4. Quality Checks
- [x] Rapikan code format dengan Black
- [x] Cek linting dengan Flake8
- [x] Cek import dan typing minimal
- [x] Pastikan tidak ada secret di code
- [x] Pastikan tidak ada debug print tersisa

## 5.5. Ketahanan Sistem
- [ ] Uji command berturut-turut
- [ ] Uji restart aplikasi dan pastikan data user tetap ada
- [ ] Uji recovery setelah error scraping
- [ ] Uji restart scheduler

**✅ CHECKLIST FASE 5:**
- [x] Unit test dasar tersedia
- [ ] Integration test utama tersedia
- [ ] Manual test selesai
- [x] Code quality check selesai
- [x] Tidak ada bug mayor yang tersisa dari diagnostics/lint/test saat ini
- [x] Commit dan push sudah dilakukan

---

# FASE 6: Deployment
**Estimasi Waktu:** 2-4 jam  
**Tujuan:** Menjalankan bot 24/7 di server/hosting

## 6.1. Pilih Platform Deployment
**Opsi yang cocok:**
- [ ] Railway
- [ ] Render
- [ ] PythonAnywhere
- [ ] VPS sendiri

**Pertimbangan memilih:**
- [ ] Support Python background worker
- [ ] Support environment variables
- [ ] Mudah restart jika crash
- [ ] Ada persistent storage atau external DB

## 6.2. Persiapan Deploy
- [x] Pastikan `requirements.txt` final untuk tahap MVP awal
- [x] Pastikan `.env.example` update
- [x] Pastikan `README.md` punya langkah setup dasar
- [x] Pastikan entrypoint jelas (`main.py`)

## 6.3. Konfigurasi Environment di Server
- [ ] Set `TELEGRAM_BOT_TOKEN`
- [ ] Set `ADMIN_CHAT_ID`
- [ ] Set `DATABASE_PATH`
- [ ] Set `BROADCAST_TIME`
- [ ] Set `TIMEZONE`

## 6.4. Deployment Checklist
- [x] Upload/push code ke repository GitHub
- [ ] Connect repository ke platform hosting
- [ ] Set start command
- [ ] Jalankan deploy pertama
- [ ] Cek logs startup
- [ ] Test bot respond `/start`
- [ ] Test scheduler aktif setelah Fase 4 selesai

## 6.5. Setelah Deploy
- [ ] Pantau logs 1-2 hari pertama
- [ ] Test broadcast harian
- [ ] Simulasikan error kecil dan pastikan bot recover
- [ ] Verifikasi data database tetap persist setelah restart

**✅ CHECKLIST FASE 6:**
- [ ] Platform deploy dipilih
- [ ] Environment variables di server lengkap
- [ ] Bot berhasil online 24/7
- [ ] Scheduler jalan di server
- [ ] Logging server terpantau
- [ ] Commit/dokumentasi deployment selesai

---

# FASE 7: Monitoring & Maintenance
**Estimasi Waktu:** ongoing  
**Tujuan:** Menjaga bot tetap stabil setelah live

## 7.1. Monitoring Dasar
- [ ] Monitor log error harian
- [ ] Cek apakah broadcast terkirim sesuai jadwal
- [ ] Cek apakah scraping masih valid
- [ ] Cek storage database dan ukuran log

## 7.2. Backup & Recovery
- [ ] Backup database otomatis harian
- [ ] Simpan beberapa versi backup
- [ ] Uji restore dari backup
- [ ] Dokumentasikan prosedur recovery

## 7.3. Admin Alert
- [ ] Kirim notifikasi ke admin jika bot gagal start
- [ ] Kirim notifikasi jika scraping gagal berulang
- [ ] Kirim ringkasan harian jumlah user/broadcast (optional)

## 7.4. Maintenance Berkala
- [ ] Update dependency jika ada security patch
- [ ] Review struktur HTML target secara berkala
- [ ] Bersihkan user invalid/inactive jika perlu
- [ ] Tinjau performa jika user bertambah

## 7.5. Roadmap Pengembangan Lanjutan
- [ ] Support banyak daerah per user
- [ ] Support filter komoditas favorit
- [ ] Simpan histori harga harian
- [ ] Buat grafik perubahan harga
- [ ] Tambah command admin
- [ ] Tambah export CSV/PDF

**✅ CHECKLIST FASE 7:**
- [ ] Monitoring dasar aktif
- [ ] Backup berjalan
- [ ] Alert admin tersedia
- [ ] Prosedur recovery terdokumentasi
- [ ] Roadmap lanjutan disusun

---

# PRIORITAS IMPLEMENTASI PALING MASUK AKAL

## Tahap 1 — Wajib dikerjakan dulu
1. Fase 0
2. Fase 1
3. Fase 2
4. Fase 3

## Tahap 2 — Agar bot benar-benar berguna
5. Fase 4
6. Fase 5

## Tahap 3 — Agar bot siap dipakai publik
7. Fase 6
8. Fase 7

---

# REKOMENDASI PRAKTIS

## Jika ingin mulai cepat versi MVP:
Kerjakan minimal ini dulu:
- [ ] Setup `.env`
- [ ] Basic bot `/start`, `/help`, `/cek`
- [ ] Scraper yang berhasil untuk 1-3 daerah
- [ ] SQLite simpan `chat_id` + `kode_daerah`
- [ ] Scheduler harian
- [ ] Logging dasar

## Jika ingin versi yang lebih aman untuk production:
Tambahkan ini sebelum publish luas:
- [ ] Error handler global
- [ ] Retry scraping
- [ ] Backup database
- [ ] Monitoring admin
- [ ] Unit test dasar
- [ ] Message split jika data panjang

---

# DEFINISI SELESAI (Definition of Done)
Project bisa dianggap siap dipakai jika:
- [ ] User bisa daftar dan pilih daerah
- [ ] User bisa cek harga manual kapan saja
- [ ] Bot bisa kirim update otomatis harian
- [ ] Data user tetap aman setelah bot restart
- [ ] Error umum tidak membuat bot mati total
- [ ] Ada log yang cukup untuk debug
- [ ] Deploy berjalan stabil minimal beberapa hari

---

# CATATAN TAMBAHAN PENTING

1. `pd.read_html` memang cepat untuk awal, tapi rentan jika struktur website berubah.
2. SQLite cukup untuk awal, tapi jika user sudah banyak, pertimbangkan PostgreSQL.
3. Jangan gabungkan semua logic ke `main.py`. Pisahkan sejak awal.
4. Fitur broadcast adalah bagian paling rawan error, jadi uji perlahan.
5. Gunakan satu sumber daftar daerah agar tidak mismatch antara keyboard, database, dan scraper.

---

# NEXT ACTION YANG PALING DISARANKAN

Urutan kerja paling aman untuk Anda mulai sekarang:
1. Rapikan `to-do.md` menjadi referensi singkat
2. Pakai `TODO_DETAIL.md` ini sebagai checklist implementasi
3. Mulai dari Fase 0
4. Setelah Fase 2 selesai, lakukan validasi hasil scraping nyata
5. Baru lanjut integrasi bot + database