"""Daily broadcast service."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from datetime import date
from typing import Any

from telegram import Bot
from telegram.error import BadRequest, Forbidden, TelegramError

from config.constants import DAERAH_LIST
from config.settings import BROADCAST_SEND_DELAY
from src.bot.admin import notify_admin
from src.database.operations import get_all_subscribed_users, set_subscription_status
from src.scraper.siskaperbapo import scrape_harga
from src.utils.formatters import format_harga_message, split_long_message
from src.utils.logger import logger


def group_users_by_region(
    users: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Group subscribed users by selected region."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for user in users:
        kode_daerah = str(user.get("kode_daerah") or "")
        if kode_daerah:
            grouped[kode_daerah].append(user)
    return dict(grouped)


async def send_price_message(
    bot: Bot,
    chat_id: int,
    message: str,
) -> bool:
    """Send a possibly long price message to one chat."""
    try:
        for chunk in split_long_message(message):
            await bot.send_message(chat_id=chat_id, text=chunk)
            await asyncio.sleep(BROADCAST_SEND_DELAY)
        return True
    except (Forbidden, BadRequest):
        logger.warning("User chat_id=%s unavailable; unsubscribing", chat_id)
        set_subscription_status(chat_id, False)
        return False
    except TelegramError:
        logger.exception("Telegram error while sending to chat_id=%s", chat_id)
        return False


async def broadcast_daily_prices(bot: Bot) -> dict[str, int]:
    """Broadcast latest prices to all subscribed users."""
    users = get_all_subscribed_users()
    grouped_users = group_users_by_region(users)
    today = date.today()

    total_users = len(users)
    success_count = 0
    failed_count = 0

    logger.info(
        "Starting daily broadcast for %s user(s), %s region(s)",
        total_users,
        len(grouped_users),
    )

    for kode_daerah, region_users in grouped_users.items():
        records = await asyncio.to_thread(scrape_harga, kode_daerah, today)
        message = format_harga_message(kode_daerah, records, today)

        for user in region_users:
            chat_id = int(user["chat_id"])
            sent = await send_price_message(bot, chat_id, message)
            if sent:
                success_count += 1
            else:
                failed_count += 1

    summary = {
        "users": total_users,
        "regions": len(grouped_users),
        "success": success_count,
        "failed": failed_count,
    }
    logger.info("Daily broadcast finished: %s", summary)

    if total_users > 0:
        await notify_admin(
            bot,
            "📣 Broadcast harian selesai
"
            f"User: {total_users}
"
            f"Daerah: {len(grouped_users)}
"
            f"Berhasil: {success_count}
"
            f"Gagal: {failed_count}",
        )

    return summary
