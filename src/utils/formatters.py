"""Formatting helpers for Telegram messages."""

from __future__ import annotations

from datetime import date
from typing import Iterable

from config.constants import (
    DAERAH_LIST,
    DEFAULT_COMMODITY_EMOJI,
    KOMODITAS_EMOJI_MAP,
    SAFE_TELEGRAM_MESSAGE_LIMIT,
)


def get_emoji_for_commodity(name: str) -> str:
    """Return matching emoji for a commodity name."""
    lowered = name.lower()
    for keyword, emoji in KOMODITAS_EMOJI_MAP.items():
        if keyword in lowered:
            return emoji
    return DEFAULT_COMMODITY_EMOJI


def format_harga_message(
    kode_daerah: str,
    records: Iterable[dict[str, str]],
    tanggal: date | None = None,
) -> str:
    """Format scraped records into a Telegram message."""
    selected_date = tanggal or date.today()
    daerah_name = DAERAH_LIST.get(kode_daerah, kode_daerah)
    items = list(records)

    if not items:
        return (
            f"❌ Data harga belum tersedia untuk {daerah_name}.\n"
            "Silakan coba lagi nanti."
        )

    lines = [
        "🌾 Harga Komoditas Siskaperbapo",
        f"📍 Daerah: {daerah_name}",
        f"📅 Tanggal: {selected_date.strftime('%d-%m-%Y')}",
        "",
    ]

    for item in items:
        komoditas = item.get("komoditas", "-")
        satuan = item.get("satuan", "")
        harga = item.get("harga", "-")
        emoji = get_emoji_for_commodity(komoditas)
        satuan_text = f"/{satuan}" if satuan and satuan != "-" else ""
        lines.append(f"{emoji} {komoditas}: Rp {harga}{satuan_text}")

    lines.extend(
        [
            "",
            "Sumber: Siskaperbapo Jawa Timur",
        ]
    )
    return "\n".join(lines)


def split_long_message(
    message: str,
    max_length: int = SAFE_TELEGRAM_MESSAGE_LIMIT,
) -> list[str]:
    """Split long Telegram messages safely by line."""
    if len(message) <= max_length:
        return [message]

    chunks: list[str] = []
    current_lines: list[str] = []
    current_length = 0

    for line in message.splitlines():
        additional_length = len(line) + 1
        if current_lines and current_length + additional_length > max_length:
            chunks.append("\n".join(current_lines))
            current_lines = [line]
            current_length = additional_length
        else:
            current_lines.append(line)
            current_length += additional_length

    if current_lines:
        chunks.append("\n".join(current_lines))

    return chunks
