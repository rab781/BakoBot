"""Admin notification helpers."""

from __future__ import annotations

from telegram import Bot

from config.settings import ADMIN_CHAT_ID
from src.utils.logger import logger


def get_admin_chat_id() -> int | None:
    """Return configured admin chat ID if valid."""
    if not ADMIN_CHAT_ID or ADMIN_CHAT_ID == "your_admin_chat_id_here":
        return None

    try:
        return int(ADMIN_CHAT_ID)
    except ValueError:
        logger.warning("Invalid ADMIN_CHAT_ID configured: %s", ADMIN_CHAT_ID)
        return None


async def notify_admin(bot: Bot, message: str) -> None:
    """Send message to admin chat if configured."""
    admin_chat_id = get_admin_chat_id()
    if admin_chat_id is None:
        return

    try:
        await bot.send_message(chat_id=admin_chat_id, text=message)
    except Exception:
        logger.exception("Failed to send admin notification")
