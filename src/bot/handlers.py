"""Telegram command and callback handlers."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from config.constants import DAERAH_LIST, MESSAGES
from config.settings import USER_COMMAND_RATE_LIMIT, USER_COMMAND_RATE_PERIOD
from src.bot.admin import notify_admin
from src.bot.keyboards import build_region_keyboard
from src.database.operations import (
    get_user_by_chat_id,
    set_subscription_status,
    upsert_user_region,
)
from src.scraper.siskaperbapo import scrape_harga
from src.utils.formatters import format_harga_message, split_long_message
from src.utils.logger import logger
from src.utils.rate_limiter import RateLimiter

rate_limiter = RateLimiter(
    max_requests=USER_COMMAND_RATE_LIMIT, period_seconds=USER_COMMAND_RATE_PERIOD
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command and show region selection."""
    if update.effective_user:
        logger.info("User %s started the bot", update.effective_user.id)

    if update.message:
        await update.message.reply_text(MESSAGES["welcome"])
        await update.message.reply_text(
            "📍 Silakan pilih daerah Anda:",
            reply_markup=build_region_keyboard(),
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    if update.message:
        await update.message.reply_text(MESSAGES["help"])


async def daerah_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /daerah command and show region selection."""
    if update.message:
        await update.message.reply_text(
            "📍 Pilih daerah baru Anda:",
            reply_markup=build_region_keyboard(),
        )


async def region_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Save selected region from inline keyboard callback."""
    query = update.callback_query
    if not query:
        return

    await query.answer()

    data = query.data or ""
    kode_daerah = data.replace("region:", "", 1)

    if kode_daerah not in DAERAH_LIST:
        await query.edit_message_text(
            "❌ Daerah tidak valid. Silakan coba lagi dengan /daerah."
        )
        return

    user = update.effective_user
    full_name = user.full_name if user else None
    username = user.username if user else None
    message_chat = getattr(query.message, "chat", None)
    chat_id = getattr(message_chat, "id", None) or query.from_user.id

    if chat_id is None:
        await query.edit_message_text(MESSAGES["error"])
        return

    upsert_user_region(
        chat_id=chat_id,
        kode_daerah=kode_daerah,
        username=username,
        full_name=full_name,
    )

    await query.edit_message_text(
        f"✅ Daerah berhasil disimpan: {DAERAH_LIST[kode_daerah]}\n\n"
        "Gunakan /cek untuk melihat harga komoditas saat ini."
    )


async def cek_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cek command and send latest commodity prices."""
    if not update.message:
        return

    chat_id = update.effective_chat.id if update.effective_chat else None
    if chat_id is None:
        await update.message.reply_text(MESSAGES.get("error_occurred", "Terjadi kesalahan"))
        return

    if rate_limiter.is_limited(str(chat_id)):
        await update.message.reply_text(MESSAGES.get("rate_limit", "⏱️ Terlalu banyak permintaan. Mohon tunggu sebentar."))
        return

    user = get_user_by_chat_id(chat_id)
    if not user or not user.get("kode_daerah"):
        await update.message.reply_text(
            "❌ Anda belum memilih daerah. Gunakan /start atau /daerah terlebih dahulu."
        )
        return

    kode_daerah = str(user["kode_daerah"])
    loading_message = await update.message.reply_text(MESSAGES["loading"])

    records = scrape_harga(kode_daerah)
    message = format_harga_message(kode_daerah, records)

    try:
        await loading_message.delete()
    except Exception:
        logger.debug("Failed deleting loading message", exc_info=True)

    for chunk in split_long_message(message):
        await update.message.reply_text(chunk)


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stop command."""
    if not update.message or not update.effective_chat:
        return

    set_subscription_status(update.effective_chat.id, False)
    await update.message.reply_text(
        "✅ Anda berhenti berlangganan update otomatis.\n"
        "Gunakan /start kapan saja untuk berlangganan kembali."
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log uncaught errors from Telegram handlers."""
    logger.exception(
        "Unhandled Telegram error. update=%s error=%s", update, context.error
    )
    if context.bot:
        await notify_admin(context.bot, f"⚠️ ERROR pada bot:\n{context.error}")
