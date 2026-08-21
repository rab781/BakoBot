## 2024-08-13 - [Path Traversal in Visualizer]
**Vulnerability:** The `/termurah` command accepted unvalidated commodity names which were used directly to construct file paths for matplotlib's `savefig` output. This could allow for arbitrary file writes / path traversal if a user provided a payload like `../../../etc/passwd`.
**Learning:** Matplotlib's `savefig` operates directly on user-provided path fragments if not sanitized, and `temp_dir / f"chart_{name}.png"` isn't safe when `name` is unchecked.
**Prevention:** Always sanitize strings that become part of a filesystem path (e.g. `re.sub(r'[^a-z0-9_]', '_', text.lower())`).
## 2024-10-27 - [Unhandled Exception DoS via Rate Limiter]
**Vulnerability:** The `termurah_command` mistakenly called a non-existent `rate_limiter.acquire(user_id)` instead of `rate_limiter.is_limited(str(user_id))`. This caused a consistent `AttributeError` for every call. Since the global `error_handler` sends stack traces to the admin for unhandled exceptions, this allowed a trivial Denial of Service (DoS) attack spamming the admin.
**Learning:** Calling non-existent methods on utility classes creates unhandled exceptions that can be leveraged for DoS if errors are broadcasted. Additionally, the rate limiter uses string keys but was passed an integer ID, which could lead to further errors.
**Prevention:** Ensure correct API usage of utility classes (e.g., `RateLimiter.is_limited`), validate input lengths to prevent secondary DoS vectors, and use safe dictionary access (`.get()`) for dynamic messages.
## 2026-08-16 - [Wildcard Injection in SQLite LIKE Queries]
**Vulnerability:** The `get_latest_prices_for_commodity` function executed SQL `LIKE` queries using unsanitized user input (`komoditas`). While parameterized queries protected against traditional SQL injection, failing to escape `%` and `_` allowed wildcard injection, potentially leading to unintended record matching or DoS via expensive full-table scans.
**Learning:** SQLite `LIKE` clauses using parameters (e.g., `?`) still evaluate wildcard characters within the parameter string unless explicitly escaped and declared via the `ESCAPE` keyword.
**Prevention:** Always sanitize strings used in `LIKE` queries by escaping `%` and `_` characters (and the escape character itself), and append `ESCAPE '\'` to the SQL query clause.
## 2026-08-16 - [Markdown Injection in Bot Messages]
**Vulnerability:** The `/termurah` command directly interpolated user input (`komoditas`) into messages that were sent with `parse_mode="Markdown"`. If a user input contained unescaped Markdown formatting characters (e.g. `*`, `_`, `\`, `[`), it could lead to malformed Markdown, causing `telegram.error.BadRequest` and preventing the message from being sent, or potentially allowing Markdown injection.
**Learning:** Sending unsanitized user input with `parse_mode="Markdown"` in Telegram bots can easily break message formatting and result in exceptions when the Telegram API rejects the payload.
**Prevention:** Always sanitize user input intended for Markdown-formatted messages by using `telegram.helpers.escape_markdown(text, version=1)`.
