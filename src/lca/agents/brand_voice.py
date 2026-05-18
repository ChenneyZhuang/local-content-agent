"""Step 1: Find business website and social links."""

import re
from lca.tools.web_search import search, extract_urls
from lca.tools.website import probe_urls
from lca.models.schemas import BusinessInfo


def find_business(name: str) -> BusinessInfo:
    """Discover business website and Facebook page."""
    website, facebook = "", ""

    # 1. Try direct .com guess
    direct = probe_urls(name)
    if direct:
        website = direct

    # 2. Search: Canberra first, then Australia
    if not website:
        for q in [
            f'"{name}" Canberra',
            f'"{name}" ACT Australia',
            f'"{name}" Australia',
            f'"{name}" official website',
        ]:
            results = search(q, 8)
            for u in extract_urls(results):
                u = u.rstrip(".,;")
                if "facebook.com" not in u.lower() and "instagram.com" not in u.lower():
                    website = u
                    break
            if website:
                break

    # 3. Facebook
    for q in [f'"{name}" Facebook Canberra', f'"{name}" Facebook ACT', f'"{name}" Facebook']:
        results = search(q, 5)
        for u in extract_urls(results):
            u = u.rstrip(".,;")
            if "facebook.com" in u.lower() and "/public/" not in u.lower():
                facebook = u
                break
        if facebook:
            break

    return BusinessInfo(name=name, website=website or None, facebook=facebook or None)
