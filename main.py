"""Main entry point for Botbako Telegram bot."""

from __future__ import annotations

from src.database.operations import init_db
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
)

from config.settings import TELEGRAM_BOT_TOKEN, validate_required_settings
from src.bot.handlers import (
    cek_command,
    daerah_command,
    error_handler,
    help_command,
    region_callback,
    start_command,
    stop_command,
)
from src.utils.logger import logger


def build_application() -> Application:
    """Build and configure Telegram application."""
    validate_required_settings()

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cek", cek_command))
    app.add_handler(CommandHandler("daerah", daerah_command))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(CallbackQueryHandler(region_callback, pattern="^region:"))

    app.add_error_handler(error_handler)
    return app


def main() -> None:
    """Start the bot in polling mode."""
    logger.info("Initializing database...")
    init_db()

    logger.info("Starting Telegram bot...")
    app = build_application()
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
