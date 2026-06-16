# Roadmap Ringkas Bot Telegram Siskaperbapo

Dokumen ini adalah roadmap ringkas project. Untuk detail teknis, risiko, dan checklist implementasi lengkap, gunakan:

- `ANALISIS_MASALAH.md` — analisis kekurangan, risiko, dan solusi pencegahan.
- `TODO_DETAIL.md` — checklist implementasi detail per fase.

---

## 1. Ringkasan Project

Bot ini bertujuan mengambil data harga komoditas dari website Siskaperbapo Jawa Timur dan mengirimkannya ke pengguna Telegram berdasarkan daerah pilihan mereka.

### Sumber Data
- Website: Siskaperbapo Jawa Timur
- URL target: `https://siskaperbapo.jatimprov.go.id/harga/tabel/?kabkota={kode_daerah}&tanggal={YYYY-MM-DD}`
- Metode awal: web scraping tabel HTML memakai Python, `requests`, dan `pandas.read_html`

### Alur Utama
1. User membuka bot Telegram.
2. User memilih daerah.
3. Bot menyimpan `chat_id` dan `kode_daerah` user.
4. User bisa mengecek harga manual dengan `/cek`.
5. Bot mengirim update harga otomatis setiap hari sesuai jadwal.

---

## 2. Masalah Utama yang Perlu Diantisipasi

### Scraping
- Struktur HTML website target bisa berubah.
- Website bisa lambat, timeout, atau down.
- Data bisa kosong, tidak lengkap, atau berubah format.

### Bot Telegram
- Pesan bisa melebihi limit Telegram.
- Broadcast massal bisa terkena rate limit.
- User bisa spam command `/cek`.
- User bisa block bot sehingga pengiriman gagal.

### Database
- Data user hilang jika memakai dictionary in-memory.
- SQLite bisa terkunci jika akses bersamaan tidak ditangani.
- Perlu backup agar data user tidak hilang.

### Deployment
- Bot bisa mati jika hosting restart/crash.
- Scheduler bisa double-run jika ada dua instance bot.
- Token Telegram berisiko bocor jika tidak memakai `.env`.

---

## 3. Prioritas Implementasi

## Prioritas 1 — MVP Wajib Jalan
- [ ] Setup struktur project yang rapi.
- [ ] Setup `.env` untuk token Telegram dan konfigurasi.
- [ ] Buat bot dasar dengan `/start` dan `/help`.
- [ ] Buat scraper Siskaperbapo untuk minimal satu daerah.
- [ ] Format hasil scraping menjadi pesan Telegram.
- [ ] Simpan user dan daerah pilihan ke SQLite.
- [ ] Tambahkan command `/cek`.

## Prioritas 2 — Bot Siap Dipakai Harian
- [ ] Tambahkan pilihan daerah dengan inline keyboard.
- [ ] Tambahkan command `/daerah` untuk ganti daerah.
- [ ] Tambahkan command `/stop` untuk berhenti berlangganan.
- [ ] Tambahkan scheduler broadcast harian.
- [ ] Tambahkan retry saat scraping gagal.
- [ ] Tambahkan logging dasar.
- [ ] Tambahkan message splitting jika pesan terlalu panjang.

## Prioritas 3 — Bot Lebih Aman dan Stabil
- [ ] Tambahkan error handler global.
- [ ] Tambahkan rate limit per user.
- [ ] Tambahkan backup database otomatis.
- [ ] Tambahkan notifikasi error ke admin.
- [ ] Tambahkan test dasar untuk scraper, formatter, dan database.
- [ ] Siapkan deployment 24/7.

## Prioritas 4 — Fitur Lanjutan
- [ ] Support banyak daerah per user.
- [ ] Filter komoditas favorit.
- [ ] Simpan histori harga.
- [ ] Buat grafik perubahan harga.
- [ ] Export data ke CSV/PDF.
- [ ] Dashboard admin sederhana.

---

## 4. Fase Implementasi Ringkas

### Fase 0 — Setup Project
Target akhir:
- Struktur folder siap.
- Virtual environment aktif.
- Dependency terinstall.
- `.gitignore`, `.env.example`, dan `requirements.txt` tersedia.

Lihat detail di `TODO_DETAIL.md` bagian Fase 0.

### Fase 1 — Bot Dasar
Target akhir:
- Bot Telegram berhasil dibuat lewat BotFather.
- Bot bisa merespons `/start` dan `/help`.
- Token aman di `.env`.
- Logging awal aktif.

Lihat detail di `TODO_DETAIL.md` bagian Fase 1.

### Fase 2 — Scraper
Target akhir:
- URL dinamis bisa dibuat berdasarkan daerah dan tanggal.
- Data HTML bisa diambil dengan timeout dan retry.
- Tabel bisa diparse dan dibersihkan.
- Output bisa diformat menjadi pesan Telegram.

Lihat detail di `TODO_DETAIL.md` bagian Fase 2.

### Fase 3 — Database dan Integrasi Bot
Target akhir:
- User bisa memilih daerah.
- Pilihan daerah tersimpan di SQLite.
- Command `/cek`, `/daerah`, dan `/stop` berjalan.
- Error umum tidak membuat bot mati.

Lihat detail di `TODO_DETAIL.md` bagian Fase 3.

### Fase 4 — Broadcast Otomatis
Target akhir:
- Bot mengirim update harian sesuai jadwal.
- Broadcast efisien dengan scraping sekali per daerah.
- Rate limit Telegram ditangani.
- Error pengiriman ke satu user tidak menghentikan broadcast seluruh user.

Lihat detail di `TODO_DETAIL.md` bagian Fase 4.

### Fase 5 — Testing
Target akhir:
- Scraper diuji untuk beberapa daerah.
- Database diuji setelah restart.
- Alur user baru, user lama, ganti daerah, dan stop diuji.
- Bot tetap berjalan saat scraping gagal.

Lihat detail di `TODO_DETAIL.md` bagian Fase 5.

### Fase 6 — Deployment
Target akhir:
- Bot berjalan 24/7 di platform hosting.
- Environment variable server lengkap.
- Scheduler aktif di server.
- Logs bisa dipantau.

Lihat detail di `TODO_DETAIL.md` bagian Fase 6.

### Fase 7 — Monitoring dan Maintenance
Target akhir:
- Backup database berjalan.
- Error penting bisa diketahui admin.
- Scraper dipantau jika website target berubah.
- Bot siap dikembangkan lebih lanjut.

Lihat detail di `TODO_DETAIL.md` bagian Fase 7.

---

## 5. Urutan Kerja yang Disarankan

1. Baca `ANALISIS_MASALAH.md` agar memahami risiko project.
2. Kerjakan `TODO_DETAIL.md` mulai Fase 0 sampai Fase 3 untuk MVP.
3. Setelah MVP berhasil, lanjutkan Fase 4 untuk broadcast harian.
4. Sebelum dipakai publik, lakukan Fase 5 testing.
5. Setelah stabil lokal, deploy di Fase 6.
6. Setelah live, jalankan monitoring dan backup di Fase 7.

---

## 6. Definition of Done MVP

MVP dianggap selesai jika:

- [ ] Bot bisa diakses di Telegram.
- [ ] User bisa memilih daerah.
- [ ] Daerah pilihan tersimpan di database.
- [ ] User bisa menjalankan `/cek` dan menerima data harga.
- [ ] Jika data tidak tersedia, bot memberi pesan yang jelas.
- [ ] Bot tidak mati ketika scraping gagal.
- [ ] Token tidak di-hardcode di source code.

---

## 7. Catatan Penting

- Jangan mulai dari deployment sebelum scraper dan database stabil.
- Jangan memakai dictionary in-memory untuk data user kecuali hanya untuk prototype sangat awal.
- Jangan hardcode token Telegram di file Python.
- Jangan scrape terlalu sering agar tidak membebani website target.
- Dokumentasikan setiap perubahan penting agar mudah dilanjutkan.
