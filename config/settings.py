"""Application settings loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "").strip()

DATABASE_PATH = os.getenv("DATABASE_PATH", "data/botbako.db").strip()
DATABASE_FULL_PATH = PROJECT_ROOT / DATABASE_PATH

SISKAPERBAPO_BASE_URL = os.getenv(
    "SISKAPERBAPO_BASE_URL",
    "https://siskaperbapo.jatimprov.go.id/harga/tabel/",
).strip()
SCRAPING_TIMEOUT = int(os.getenv("SCRAPING_TIMEOUT", "30"))
SCRAPING_RETRY_ATTEMPTS = int(os.getenv("SCRAPING_RETRY_ATTEMPTS", "3"))

BROADCAST_TIME = os.getenv("BROADCAST_TIME", "08:00").strip()
TIMEZONE = os.getenv("TIMEZONE", "Asia/Jakarta").strip()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").strip().upper()
LOG_FILE = PROJECT_ROOT / os.getenv("LOG_FILE", "logs/bot.log").strip()

USER_COMMAND_RATE_LIMIT = int(os.getenv("USER_COMMAND_RATE_LIMIT", "5"))
USER_COMMAND_RATE_PERIOD = int(os.getenv("USER_COMMAND_RATE_PERIOD", "60"))


def validate_required_settings() -> None:
    """Validate settings needed to run the Telegram bot."""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_bot_token_here":
        raise ValueError(
            "TELEGRAM_BOT_TOKEN belum diatur. Copy .env.example ke .env "
            "lalu isi token BotFather."
        )
