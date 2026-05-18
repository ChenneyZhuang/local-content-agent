"""Web search via DuckDuckGo (free, no API key required)."""

import subprocess
import re
import os

SCRIPT = "/Volumes/SSD/scripts/web_search.py"


def search(query: str, limit: int = 5) -> str:
    """Search the web and return results as text."""
    if not os.path.exists(SCRIPT):
        # Fallback: basic urllib search
        return _fallback_search(query, limit)

    result = subprocess.run(
        ["python3", SCRIPT, query, str(limit), "--extract"],
        capture_output=True, text=True, timeout=30,
    )
    return result.stdout


def _fallback_search(query: str, limit: int = 5) -> str:
    """Minimal DuckDuckGo HTML search fallback."""
    import urllib.request
    import urllib.parse
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        # Extract result snippets
        results = re.findall(r'class="result__snippet">(.*?)</a>', html, re.DOTALL)
        text = "\n\n".join(re.sub(r"<[^>]+>", "", r).strip() for r in results[:limit])
        return text or "(no results)"
    except Exception as e:
        return f"(search failed: {e})"


def extract_urls(text: str) -> list[str]:
    """Extract URLs from text."""
    return re.findall(r"https?://[^\s)\]]+", text)
