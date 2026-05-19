"""Website content fetcher — scrapes and cleans HTML for LLM analysis."""

import re
import urllib.request


def fetch(url: str, max_chars: int = 8000) -> str:
    """Fetch and extract plain text from a website."""
    if not url:
        return ""

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; LocalContentAgent/0.1)"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # Strip scripts, styles, and HTML tags
        text = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", html)
        text = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        return text[:max_chars]
    except Exception as e:
        return f"(could not fetch: {e})"


def probe_urls(base_name: str) -> str | None:
    """Try common URL patterns for a business name. Returns first reachable URL."""
    slug = re.sub(r"[^a-zA-Z0-9]", "", base_name).lower()
    candidates = [
        f"https://{slug}.com",
        f"https://www.{slug}.com",
        f"https://{slug}.com.au",
        f"https://www.{slug}.com.au",
    ]
    for url in candidates:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            urllib.request.urlopen(req, timeout=5)
            return url
        except Exception:
            continue
    return None
