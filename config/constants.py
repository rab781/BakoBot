"""Static constants used by the bot."""

DAERAH_LIST = {
    "surabayakota": "Kota Surabaya",
    "malangkota": "Kota Malang",
    "madiunkota": "Kota Madiun",
    "kedirikota": "Kota Kediri",
    "blitarkota": "Kota Blitar",
    "mojokertokota": "Kota Mojokerto",
    "pasuruankota": "Kota Pasuruan",
    "probolinggokota": "Kota Probolinggo",
    "batukota": "Kota Batu",
    "bangkalankab": "Kab. Bangkalan",
    "banyuwangikab": "Kab. Banyuwangi",
    "blitarkab": "Kab. Blitar",
    "bojonegorokab": "Kab. Bojonegoro",
    "bondowosokab": "Kab. Bondowoso",
    "gresikkab": "Kab. Gresik",
    "jemberkab": "Kab. Jember",
    "jombangkab": "Kab. Jombang",
    "kedirikab": "Kab. Kediri",
    "lamongankab": "Kab. Lamongan",
    "lumajangkab": "Kab. Lumajang",
    "madiunkab": "Kab. Madiun",
    "magetankab": "Kab. Magetan",
    "malangkab": "Kab. Malang",
    "mojokertokab": "Kab. Mojokerto",
    "nganjukkab": "Kab. Nganjuk",
    "ngawikab": "Kab. Ngawi",
    "pacitankab": "Kab. Pacitan",
    "pamekasankab": "Kab. Pamekasan",
    "pasuruankab": "Kab. Pasuruan",
    "ponorogokab": "Kab. Ponorogo",
    "probolinggokab": "Kab. Probolinggo",
    "sampangkab": "Kab. Sampang",
    "sidoarjokab": "Kab. Sidoarjo",
    "situbondokab": "Kab. Situbondo",
    "sumenepkab": "Kab. Sumenep",
    "trenggalekkab": "Kab. Trenggalek",
    "tubankab": "Kab. Tuban",
    "tulungagungkab": "Kab. Tulungagung",
}

MESSAGES = {
    "welcome": (
        "🌾 Selamat datang di Bot Harga Komoditas Siskaperbapo Jawa Timur!\n\n"
        "Bot ini akan membantu Anda mengecek harga komoditas "
        "berdasarkan daerah pilihan.\n\n"
        "Untuk tahap awal, gunakan /help untuk melihat command yang tersedia."
    ),
    "help": (
        "📖 Panduan Bot\n\n"
        "/start - Mulai menggunakan bot\n"
        "/help - Tampilkan bantuan\n"
        "/cek - Cek harga komoditas saat ini\n"
        "/daerah - Pilih atau ganti daerah\n"
        "/stop - Berhenti menerima update otomatis\n\n"
        "Catatan: fitur /cek, /daerah, dan /stop akan aktif setelah "
        "integrasi database dan scraper selesai."
    ),
    "loading": "⏳ Mengambil data harga komoditas...",
    "not_implemented": "🚧 Fitur ini sedang disiapkan dan akan segera tersedia.",
    "error": "⚠️ Terjadi kesalahan. Silakan coba lagi nanti.",
}

KOMODITAS_EMOJI_MAP = {
    "beras": "🌾",
    "gula": "🍬",
    "minyak": "🛢️",
    "telur": "🥚",
    "ayam": "🐔",
    "daging": "🥩",
    "sapi": "🥩",
    "cabai": "🌶️",
    "cabe": "🌶️",
    "bawang": "🧅",
    "tomat": "🍅",
}

DEFAULT_COMMODITY_EMOJI = "📦"
TELEGRAM_MESSAGE_LIMIT = 4096
SAFE_TELEGRAM_MESSAGE_LIMIT = 3900
