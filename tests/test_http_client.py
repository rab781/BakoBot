import pytest
import requests
import certifi
from unittest.mock import patch, MagicMock

from src.scraper.http_client import fetch_url, post_form, _session


def test_session_verify_certifi():
    """Verify that the global session uses certifi for verification."""
    assert _session.verify == certifi.where()


@patch("src.scraper.http_client._session.get")
def test_fetch_url(mock_get):
    """Verify that fetch_url uses the session."""
    mock_response = MagicMock()
    mock_response.text = "Success"
    mock_get.return_value = mock_response

    result = fetch_url("https://example.com")

    assert result == "Success"
    mock_get.assert_called_once()
    assert mock_get.call_args[0][0] == "https://example.com"
    mock_response.raise_for_status.assert_called_once()


@patch("src.scraper.http_client._session.post")
def test_post_form(mock_post):
    """Verify that post_form uses the session."""
    mock_response = MagicMock()
    mock_response.text = "Success"
    mock_post.return_value = mock_response

    result = post_form("https://example.com", {"key": "value"})

    assert result == "Success"
    mock_post.assert_called_once()
    assert mock_post.call_args[0][0] == "https://example.com"
    assert mock_post.call_args[1]["data"] == {"key": "value"}
    mock_response.raise_for_status.assert_called_once()


def test_actual_certificate_verification():
    """Verify that a request fails on an invalid certificate.
    untrusted-root.badssl.com has a certificate signed by an untrusted CA.
    """
    with pytest.raises(requests.exceptions.SSLError):
        fetch_url("https://untrusted-root.badssl.com/")
