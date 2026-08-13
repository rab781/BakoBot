## 2024-08-13 - [Path Traversal in Visualizer]
**Vulnerability:** The `/termurah` command accepted unvalidated commodity names which were used directly to construct file paths for matplotlib's `savefig` output. This could allow for arbitrary file writes / path traversal if a user provided a payload like `../../../etc/passwd`.
**Learning:** Matplotlib's `savefig` operates directly on user-provided path fragments if not sanitized, and `temp_dir / f"chart_{name}.png"` isn't safe when `name` is unchecked.
**Prevention:** Always sanitize strings that become part of a filesystem path (e.g. `re.sub(r'[^a-z0-9_]', '_', text.lower())`).
