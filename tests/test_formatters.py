"""Tests for Telegram message formatters."""

from src.utils.formatters import (
    format_harga_message,
    get_emoji_for_commodity,
    split_long_message,
)


def test_get_emoji_for_commodity_matches_keyword() -> None:
    assert get_emoji_for_commodity("Beras Premium") == "🌾"
    assert get_emoji_for_commodity("Cabai Rawit") == "🌶️"


def test_format_harga_message_contains_region_and_item() -> None:
    message = format_harga_message(
        "surabayakota",
        [
            {
                "komoditas": "Beras Premium",
                "satuan": "Kg",
                "harga": "15.000",
            }
        ],
    )

    assert "Kota Surabaya" in message
    assert "Beras Premium" in message
    assert "15.000" in message


def test_split_long_message_splits_by_limit() -> None:
    message = "baris\n" * 100
    chunks = split_long_message(message, max_length=50)

    assert len(chunks) > 1
    assert all(len(chunk) <= 50 for chunk in chunks)
