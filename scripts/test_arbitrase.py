"""Script to populate database for arbitrage testing."""

import asyncio
from datetime import date
from src.scraper.siskaperbapo import scrape_harga
from src.database.operations import save_price_histories

# 5 daerah sampel
DAERAH_TEST = ["jemberkab", "surabayakota", "malangkota", "banyuwangikab", "situbondokab"]

async def main():
    print("Mulai mengambil sampel data dari 5 daerah untuk testing...")
    today = date.today()
    tanggal_str = today.strftime("%Y-%m-%d")
    
    for daerah in DAERAH_TEST:
        print(f"Mengambil data dari: {daerah}...")
        records = scrape_harga(daerah, today)
        if records:
            history_records = []
            for r in records:
                try:
                    harga_raw = str(r.get("harga", "0")).replace(".", "").replace(",", "").strip()
                    harga_int = int(harga_raw) if harga_raw.isdigit() else 0
                    if harga_int > 0:
                        history_records.append((
                            tanggal_str,
                            daerah,
                            r.get("komoditas", ""),
                            harga_int
                        ))
                except Exception:
                    pass
            if history_records:
                save_price_histories(history_records)
    print("Selesai! Sekarang coba ketik '/termurah beras premium' di Telegram.")

if __name__ == "__main__":
    asyncio.run(main())
