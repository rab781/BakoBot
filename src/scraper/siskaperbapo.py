"""High-level Siskaperbapo scraper service."""

from __future__ import annotations

from datetime import date
from typing import Optional

import requests

from src.scraper.http_client import fetch_url
from src.scraper.parser import extract_records_from_html
from src.scraper.url_builder import build_url
from src.utils.logger import logger


def scrape_harga(
    kode_daerah: str,
    tanggal: Optional[date] = None,
) -> list[dict[str, str]]:
    """Scrape commodity prices for a region and date."""
    url = build_url(kode_daerah, tanggal)

    try:
        html = fetch_url(url)
        records = extract_records_from_html(html)
        logger.info("Scraped %s record(s) for %s", len(records), kode_daerah)
        return records
    except requests.RequestException as exc:
        logger.exception("HTTP scraping failed for %s: %s", kode_daerah, exc)
        return []
    except Exception as exc:
        logger.exception("Unexpected scraping failure for %s: %s", kode_daerah, exc)
        return []
