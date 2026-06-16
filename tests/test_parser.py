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


def test_extract_records_from_siskaperbapo_ajax_table() -> None:
    html = """
    <table>
        <tr>
            <th>NO</th>
            <th>NAMA BAHAN POKOK</th>
            <th>SATUAN</th>
            <th>HARGA KEMARIN</th>
            <th>HARGA SEKARANG</th>
            <th>PERUBAHAN (Rp)</th>
            <th>PERUBAHAN (%)</th>
        </tr>
        <tr>
            <td>01</td>
            <td>BERAS</td>
            <td></td>
            <td>0</td>
            <td>0</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>- Beras Premium</td>
            <td>kg</td>
            <td>15.800</td>
            <td>15.900</td>
            <td>100</td>
            <td>0.63</td>
        </tr>
    </table>
    """

    records = extract_records_from_html(html)

    assert len(records) == 1
    assert records[0]["komoditas"] == "Beras Premium"
    assert records[0]["satuan"] == "kg"
    assert records[0]["harga"] == "15.900"
