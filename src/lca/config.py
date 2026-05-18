"""Configuration from environment variables."""

import os
from pathlib import Path


# LLM
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
LLM_MODEL = os.getenv("LCA_LLM_MODEL", "deepseek-chat")

# Perplexity (optional)
PERPLEXITY_ENABLED = os.getenv("PERPLEXITY_ENABLED", "").lower() in ("1", "true", "yes")
CDP_URL = os.getenv("LCA_CDP_URL", "http://localhost:9222")

# Output
OUTPUT_DIR = Path(os.getenv("LCA_OUTPUT_DIR", "./output"))

# Limits
MAX_TOPICS = int(os.getenv("LCA_MAX_TOPICS", "8"))
RESEARCH_TIMEOUT = int(os.getenv("LCA_RESEARCH_TIMEOUT", "300"))
