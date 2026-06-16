"""Tests for HTML table parser."""

from src.scraper.parser import extract_records_from_html


def test_extract_records_from_html_table() -> None:
    html = """
    <table>
        <tr><th>No</th><th>Komoditas</th><th>Satuan</th><th>Harga</th></tr>
        <tr><td>1</td><td>Beras Premium</td><td>Kg</td><td>15000</td></tr>
    </table>
    """

    records = extract_records_from_html(html)

    assert len(records) == 1
    assert records[0]["komoditas"] == "Beras Premium"
    assert records[0]["satuan"] == "Kg"
    assert records[0]["harga"] == "15000"
