"""Database backup helpers."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from config.settings import BACKUP_DIR, BACKUP_KEEP_COUNT, DATABASE_FULL_PATH
from src.utils.logger import logger


def backup_database() -> Path | None:
    """Create a timestamped SQLite database backup."""
    if not DATABASE_FULL_PATH.exists():
        logger.warning("Database backup skipped; database does not exist yet")
        return None

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"botbako_{timestamp}.db"
    shutil.copy2(DATABASE_FULL_PATH, backup_path)
    logger.info("Database backup created: %s", backup_path)
    cleanup_old_backups()
    return backup_path


def cleanup_old_backups() -> None:
    """Keep only newest database backups based on configured limit."""
    backups = sorted(BACKUP_DIR.glob("botbako_*.db"), reverse=True)
    for backup in backups[BACKUP_KEEP_COUNT:]:
        backup.unlink(missing_ok=True)
        logger.info("Old database backup removed: %s", backup)
