"""URL builder for Siskaperbapo requests."""

from __future__ import annotations

from datetime import date
from typing import Optional
from urllib.parse import urlencode

from config.settings import SISKAPERBAPO_BASE_URL


def build_url(kode_daerah: str, tanggal: Optional[date] = None) -> str:
    """Build Siskaperbapo table URL for a region and date."""
    selected_date = tanggal or date.today()
    query = urlencode(
        {
            "kabkota": kode_daerah,
            "tanggal": selected_date.strftime("%Y-%m-%d"),
        }
    )
    return f"{SISKAPERBAPO_BASE_URL}?{query}"
