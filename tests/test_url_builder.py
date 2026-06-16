"""Tests for Siskaperbapo URL builder."""

from datetime import date

from src.scraper.url_builder import build_url


def test_build_url_contains_region_and_date() -> None:
    url = build_url("surabayakota", date(2024, 1, 15))

    assert "kabkota=surabayakota" in url
    assert "tanggal=2024-01-15" in url
