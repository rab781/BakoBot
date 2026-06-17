"""Main entry point for Botbako Telegram bot."""

from __future__ import annotations

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.database.operations import init_db
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
)

from config.settings import (
    BROADCAST_TIME,
    TELEGRAM_BOT_TOKEN,
    TIMEZONE,
    validate_required_settings,
)
from src.bot.broadcast import broadcast_daily_prices
from src.database.backup import backup_database
from src.bot.handlers import (
    cek_command,
    daerah_command,
    error_handler,
    help_command,
    region_callback,
    start_command,
    stop_command,
    termurah_command,
)
from src.utils.logger import logger


async def post_init(app: Application) -> None:
    """Setup and start background scheduler after the bot has started."""
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    
    hour, minute = map(int, BROADCAST_TIME.split(":"))
    scheduler.add_job(
        broadcast_daily_prices,
        "cron",
        hour=hour,
        minute=minute,
        args=[app.bot],
        id="daily_broadcast",
        replace_existing=True,
    )

    async def run_backup():
        await asyncio.to_thread(backup_database)

    scheduler.add_job(
        run_backup,
        "cron",
        hour=0,
        minute=0,
        id="daily_backup",
        replace_existing=True,
    )
    
    scheduler.start()
    logger.info("Scheduler started. Broadcast at %s, Backup at 00:00", BROADCAST_TIME)


def build_application() -> Application:
    """Build and configure Telegram application."""
    validate_required_settings()

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cek", cek_command))
    app.add_handler(CommandHandler("termurah", termurah_command))
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
