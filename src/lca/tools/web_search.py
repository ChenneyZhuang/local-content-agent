"""Web search — uses the websearch package if installed, falls back to built-in DuckDuckGo."""

import re
import urllib.request
import urllib.parse

# Prefer the websearch package
try:
    from websearch.engine import search as _package_search
    _has_package = True
except ImportError:
    _has_package = False


def search(query: str, limit: int = 5) -> str:
    """Search the web and return results as text."""
    if _has_package:
        results = _package_search(query, limit)
        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. {r['title']}\n   {r['url']}")
        return "\n\n".join(lines)

    # Built-in fallback: DuckDuckGo HTML search (zero dependencies)
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        results = re.findall(
            r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )
        lines = []
        for u, t in results[:limit]:
            title = re.sub(r"<[^>]+>", "", t).strip()
            # Decode DuckDuckGo redirect URLs
            clean_url = u
            if "uddg=" in clean_url:
                clean_url = clean_url.split("uddg=")[1]
                for sep in ("&rut=", "&amp;rut=", "?rut="):
                    if sep in clean_url:
                        clean_url = clean_url.split(sep)[0]
                        break
                clean_url = urllib.parse.unquote(clean_url)
            lines.append(f"{len(lines)+1}. {title}\n   {clean_url}")
        return "\n\n".join(lines) if lines else "(no results)"
    except Exception as e:
        return f"(search failed: {e})"


def extract_urls(text: str) -> list[str]:
    """Extract URLs from text."""
    return re.findall(r"https?://[^\s)\]]+", text)
