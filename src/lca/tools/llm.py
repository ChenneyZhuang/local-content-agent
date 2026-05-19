"""LLM API client — OpenAI-compatible (DeepSeek by default)."""

import json
import time
import urllib.request
from lca.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, LLM_MODEL

_last_call = 0


def _rate_limit(interval: float = 1.5):
    global _last_call
    elapsed = time.time() - _last_call
    if elapsed < interval:
        time.sleep(interval - elapsed)
    _last_call = time.time()


def chat(prompt: str, system: str = "", max_tokens: int = 4096) -> str:
    """Call the LLM and return the response text."""
    if not DEEPSEEK_API_KEY:
        raise RuntimeError(
            "DEEPSEEK_API_KEY not set. Run: export DEEPSEEK_API_KEY=sk-..."
        )

    _rate_limit()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    body = json.dumps(
        {
            "model": LLM_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
    ).encode()

    req = urllib.request.Request(
        f"{DEEPSEEK_BASE_URL}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"LLM API error: {e}")
