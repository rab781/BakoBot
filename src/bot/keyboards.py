"""Telegram inline keyboard helpers."""

from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config.constants import DAERAH_LIST


def build_region_keyboard(columns: int = 2) -> InlineKeyboardMarkup:
    """Build inline keyboard for region selection."""
    buttons = [
        InlineKeyboardButton(name, callback_data=f"region:{code}")
        for code, name in DAERAH_LIST.items()
    ]

    rows = [
        buttons[index : index + columns] for index in range(0, len(buttons), columns)
    ]
    return InlineKeyboardMarkup(rows)
