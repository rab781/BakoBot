## 2024-05-24 - SQLite Batch Inserts are Critical for Broadcasting
**Learning:** During the daily broadcast process (`broadcast_daily_prices`), the bot scrapes ~100 commodities across potentially dozens of regions. When saving these to the SQLite `price_history` table, using sequential `conn.execute()` for each commodity record took ~0.6 seconds per 500 records. Using `conn.executemany()` to batch insert all records for a region at once reduced this to ~0.003 seconds. Since `broadcast_daily_prices` is expected to scale as more regions and users are added, batching these writes drastically reduces database locking and broadcast delays.
**Action:** When inserting multiple rows into SQLite inside loops (such as during scraping or broadcasting), always collect the rows into a list and use `executemany()` instead of individual `execute()` calls to prevent severe performance bottlenecks.

## 2026-08-16 - HTTP Keep-Alive for Scraping
**Learning:** During the scraping process, repeatedly issuing `requests.get` or `requests.post` creates a new TCP connection for every request, which introduces significant latency (approx. 1.5s vs 0.15s per 5 requests in this case). Using a global `requests.Session()` reuses the underlying connection (HTTP Keep-Alive), drastically reducing connection overhead.
**Action:** When performing sequential API calls or scraping to the same host, always use a single `requests.Session()` instead of repeated bare `requests.get` / `requests.post` calls to utilize connection pooling and avoid repeating SSL/TCP handshakes.

## 2026-08-17 - BeautifulSoup Parser Performance
**Learning:** When parsing large HTML tables, `BeautifulSoup(html, "html.parser")` is noticeably slower than `BeautifulSoup(html, "lxml")`. "lxml" uses a C-based parser which is heavily optimized for speed, resulting in faster parsing, especially when extracting large sets of commodity records in `extract_records_with_beautifulsoup`.
**Action:** Always prefer the `lxml` parser over `html.parser` when using BeautifulSoup if `lxml` is available in the environment to significantly improve parsing performance.
