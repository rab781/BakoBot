"""HTTP client used by scraper."""

from __future__ import annotations

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from config.settings import SCRAPING_RETRY_ATTEMPTS, SCRAPING_TIMEOUT
from src.utils.logger import logger


class ScrapingError(Exception):
    """Raised when scraping cannot be completed."""


def _default_headers() -> dict[str, str]:
    """Return browser-like default headers."""
    return {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        )
    }


@retry(
    stop=stop_after_attempt(SCRAPING_RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.RequestException),
    reraise=True,
)
def fetch_url(url: str) -> str:
    """Fetch URL with timeout and retry."""
    logger.info("Fetching URL: %s", url)
    response = requests.get(
        url,
        timeout=SCRAPING_TIMEOUT,
        headers=_default_headers(),
    )
    response.raise_for_status()
    return response.text


@retry(
    stop=stop_after_attempt(SCRAPING_RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.RequestException),
    reraise=True,
)
def post_form(url: str, data: dict[str, str]) -> str:
    """POST form data with timeout and retry."""
    logger.info("Posting form to URL: %s", url)
    response = requests.post(
        url,
        data=data,
        timeout=SCRAPING_TIMEOUT,
        headers=_default_headers(),
    )
    response.raise_for_status()
    return response.text
