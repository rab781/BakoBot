"""Parser and cleaner for Siskaperbapo HTML tables."""

from __future__ import annotations

from io import StringIO
from typing import Any, cast

import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag

from src.utils.logger import logger

EMPTY_VALUES = {"", "-", "nan", "none", "None"}


def parse_html_tables(html: str) -> list[pd.DataFrame]:
    """Parse all HTML tables from a response body using pandas fallback."""
    try:
        tables = pd.read_html(StringIO(html))
    except ValueError:
        logger.warning("No HTML table found in response")
        return []

    logger.info("Found %s HTML table(s)", len(tables))
    return tables


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean empty rows/columns and normalize text values."""
    cleaned = df.copy()
    cleaned = cleaned.dropna(how="all")
    cleaned = cleaned.dropna(axis=1, how="all")

    for column in cleaned.columns:
        cleaned[column] = cleaned[column].astype(str).str.strip()

    cleaned = cleaned[~cleaned.isin(["", "-", "nan", "None"]).all(axis=1)]
    cleaned = cast(pd.DataFrame, cleaned)
    logger.info("Cleaned DataFrame shape: %s", cleaned.shape)
    return cleaned


def _clean_text(value: str) -> str:
    """Normalize whitespace from HTML text."""
    return " ".join(value.replace("\xa0", " ").split()).strip()


def _normalize_price(value: Any) -> str:
    """Normalize raw price value to display string."""
    text = _clean_text(str(value))
    if text.lower() in EMPTY_VALUES:
        return "-"
    return text


def _clean_commodity_name(value: str) -> str:
    """Remove visual indentation markers from commodity names."""
    return _clean_text(value).lstrip("- ").strip()


def _is_empty(value: str) -> bool:
    """Check whether text is considered empty."""
    return value.strip().lower() in {"", "-", "nan", "none"}


def extract_records_with_beautifulsoup(html: str) -> list[dict[str, str]]:
    """Extract records directly from HTML table while preserving displayed text."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not isinstance(table, Tag):
        return []

    records: list[dict[str, str]] = []
    rows = table.find_all("tr")

    for row in rows:
        if not isinstance(row, Tag):
            continue
        cells = row.find_all(["td", "th"])
        if len(cells) < 5:
            continue

        values = [_clean_text(cell.get_text(" ", strip=True)) for cell in cells]
        lowered = " ".join(values).lower()
        if "nama bahan pokok" in lowered and "harga sekarang" in lowered:
            continue

        komoditas = _clean_commodity_name(values[1])
        satuan = _clean_text(values[2])
        harga = _normalize_price(values[4])

        if _is_empty(komoditas) or _is_empty(satuan):
            continue

        records.append(
            {
                "komoditas": komoditas,
                "satuan": satuan,
                "harga": harga,
            }
        )

    if records:
        logger.info("Extracted %s record(s) using BeautifulSoup", len(records))

    return records


def dataframe_to_records(df: pd.DataFrame) -> list[dict[str, str]]:
    """Convert cleaned dataframe rows to generic commodity records."""
    records: list[dict[str, str]] = []

    if df.empty or len(df.columns) < 2:
        return records

    for _, row in df.iterrows():
        values = [str(value).strip() for value in row.tolist()]
        if not values or all(value.lower() in EMPTY_VALUES for value in values):
            continue

        lowered = " ".join(values).lower()
        if "komoditas" in lowered and "harga" in lowered:
            continue

        komoditas = _clean_commodity_name(values[1] if len(values) > 1 else values[0])
        satuan = values[2] if len(values) > 2 else ""
        harga_index = 4 if len(values) > 4 else -1
        harga = _normalize_price(values[harga_index])

        if _is_empty(komoditas) or _is_empty(satuan):
            continue

        records.append(
            {
                "komoditas": komoditas,
                "satuan": satuan,
                "harga": harga,
            }
        )

    return records


def extract_records_from_html(html: str) -> list[dict[str, str]]:
    """Extract commodity records from HTML table."""
    bs4_records = extract_records_with_beautifulsoup(html)
    if bs4_records:
        return bs4_records

    for table in parse_html_tables(html):
        cleaned = clean_dataframe(table)
        records = dataframe_to_records(cleaned)
        if records:
            return records

    return []
