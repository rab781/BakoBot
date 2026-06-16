"""Parser and cleaner for Siskaperbapo HTML tables."""

from __future__ import annotations

from io import StringIO
from typing import Any, cast

import pandas as pd

from src.utils.logger import logger


def parse_html_tables(html: str) -> list[pd.DataFrame]:
    """Parse all HTML tables from a response body."""
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


def _normalize_price(value: Any) -> str:
    """Normalize raw price value to display string."""
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "-"}:
        return "-"
    return text


def dataframe_to_records(df: pd.DataFrame) -> list[dict[str, str]]:
    """Convert cleaned dataframe rows to generic commodity records."""
    records: list[dict[str, str]] = []

    if df.empty or len(df.columns) < 2:
        return records

    for _, row in df.iterrows():
        values = [str(value).strip() for value in row.tolist()]
        if not values or all(
            value.lower() in {"", "nan", "none", "-"} for value in values
        ):
            continue

        lowered = " ".join(values).lower()
        if "komoditas" in lowered and "harga" in lowered:
            continue

        komoditas = values[1] if len(values) > 1 else values[0]
        satuan = values[2] if len(values) > 2 else ""
        harga = _normalize_price(values[3] if len(values) > 3 else values[-1])

        if komoditas.lower() in {"nan", "none", "", "-"}:
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
    """Extract commodity records from the first useful table in HTML."""
    for table in parse_html_tables(html):
        cleaned = clean_dataframe(table)
        records = dataframe_to_records(cleaned)
        if records:
            return records

    return []
