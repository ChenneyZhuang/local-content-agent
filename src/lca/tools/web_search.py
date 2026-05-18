"""Web search — uses the websearch package if installed, falls back to local script."""

import re
import subprocess
import os

# Prefer the websearch package
try:
    from websearch.engine import search as _package_search
    _has_package = True
except ImportError:
    _has_package = False

SCRIPT = "/Volumes/SSD/scripts/web_search.py"


def search(query: str, limit: int = 5) -> str:
    """Search the web and return results as text."""
    if _has_package:
        results = _package_search(query, limit)
        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. {r['title']}\n   {r['url']}")
        return "\n\n".join(lines)

    # Fallback to local script
    if os.path.exists(SCRIPT):
        result = subprocess.run(
            ["python3", SCRIPT, query, str(limit)],
            capture_output=True, text=True, timeout=30,
        )
        return result.stdout

    # Last resort: basic urllib
    import urllib.request, urllib.parse
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        results = re.findall(r'class="result__snippet">(.*?)</a>', html, re.DOTALL)
        return "\n\n".join(re.sub(r"<[^>]+>", "", r).strip() for r in results[:limit])
    except Exception as e:
        return f"(search failed: {e})"


def extract_urls(text: str) -> list[str]:
    """Extract URLs from text."""
    return re.findall(r"https?://[^\s)\]]+", text)
