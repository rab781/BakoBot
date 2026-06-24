# Botbako - Bot Telegram Siskaperbapo

Bot Telegram untuk mengambil dan mengirimkan informasi harga komoditas dari Siskaperbapo Jawa Timur berdasarkan daerah pilihan pengguna.

## Setup Lokal

1. Buat virtual environment.
2. Install dependency dari `requirements.txt`.
3. Copy `.env.example` menjadi `.env`.
4. Isi `TELEGRAM_BOT_TOKEN` dari BotFather.
5. Jalankan bot dengan `python main.py`.

## Command Bot Rencana

- `/start` untuk mulai dan memilih daerah.
- `/help` untuk bantuan.
- `/cek` untuk cek harga saat ini.
- `/daerah` untuk mengganti daerah.
- `/stop` untuk berhenti berlangganan.
