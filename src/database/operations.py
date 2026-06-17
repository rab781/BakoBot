"""SQLite database operations."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from config.settings import DATABASE_FULL_PATH
from src.utils.logger import logger


def get_connection() -> sqlite3.Connection:
    """Create SQLite connection with row access by column name."""
    Path(DATABASE_FULL_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_FULL_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Initialize database tables."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                kode_daerah TEXT,
                is_subscribed INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_users_subscribed ON users(is_subscribed)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_users_kode_daerah ON users(kode_daerah)"
        )
        
        # Tabel histori harga
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT NOT NULL,
                kode_daerah TEXT NOT NULL,
                komoditas TEXT NOT NULL,
                harga_int INTEGER NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_price_history_tanggal_komoditas ON price_history(tanggal, komoditas)"
        )
    logger.info("Database initialized at %s", DATABASE_FULL_PATH)


def upsert_user_region(
    chat_id: int,
    kode_daerah: str,
    username: str | None = None,
    full_name: str | None = None,
) -> None:
    """Create or update user region preference."""
    now = datetime.utcnow().isoformat()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO users (
                chat_id, username, full_name, kode_daerah,
                is_subscribed, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, 1, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET
                username = excluded.username,
                full_name = excluded.full_name,
                kode_daerah = excluded.kode_daerah,
                is_subscribed = 1,
                updated_at = excluded.updated_at
            """,
            (chat_id, username, full_name, kode_daerah, now, now),
        )
    logger.info(
        "Saved region for chat_id=%s kode_daerah=%s",
        chat_id,
        kode_daerah,
    )


def get_user_by_chat_id(chat_id: int) -> dict[str, Any] | None:
    """Get user by Telegram chat ID."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE chat_id = ?",
            (chat_id,),
        ).fetchone()
    return dict(row) if row else None


def set_subscription_status(chat_id: int, is_subscribed: bool) -> None:
    """Update subscription status for a user."""
    now = datetime.utcnow().isoformat()
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET is_subscribed = ?, updated_at = ? WHERE chat_id = ?",
            (1 if is_subscribed else 0, now, chat_id),
        )
    logger.info(
        "Updated subscription chat_id=%s subscribed=%s",
        chat_id,
        is_subscribed,
    )


def get_all_subscribed_users() -> list[dict[str, Any]]:
    """Get all users subscribed to daily broadcast."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM users
            WHERE is_subscribed = 1
              AND kode_daerah IS NOT NULL
              AND kode_daerah != ''
            """
        ).fetchall()
    return [dict(row) for row in rows]


def save_price_history(tanggal: str, kode_daerah: str, komoditas: str, harga_int: int) -> None:
    """Save scraped price to history."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO price_history (tanggal, kode_daerah, komoditas, harga_int)
            VALUES (?, ?, ?, ?)
            """,
            (tanggal, kode_daerah, komoditas, harga_int),
        )


def get_latest_prices_for_commodity(komoditas: str) -> list[dict[str, Any]]:
    """Get the latest prices for a specific commodity across all regions."""
    with get_connection() as conn:
        # Cari tanggal terbaru untuk komoditas ini
        row = conn.execute(
            "SELECT MAX(tanggal) as max_date FROM price_history WHERE komoditas LIKE ?",
            (f"%{komoditas}%",)
        ).fetchone()
        
        max_date = row["max_date"] if row else None
        if not max_date:
            return []
            
        rows = conn.execute(
            """
            SELECT kode_daerah, komoditas, harga_int 
            FROM price_history 
            WHERE komoditas LIKE ? AND tanggal = ?
            ORDER BY harga_int ASC
            """,
            (f"%{komoditas}%", max_date)
        ).fetchall()
        
    return [dict(row) for row in rows]
