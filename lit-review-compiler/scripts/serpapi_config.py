"""Optional SerpApi key loader for lit-review-compiler.

Looks for settings.json next to this file (i.e. lit-review-compiler/settings.json,
sibling to scripts/). Its absence, malformed JSON, or a missing/empty
serpapi_key all resolve to None rather than raising -- callers treat None as
"no Google Scholar enhancement available this run" and fall back silently to
their existing behavior.
"""

import json
import os

_SETTINGS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "settings.json")


def get_serpapi_key():
    try:
        with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None
    key = data.get("serpapi_key") if isinstance(data, dict) else None
    if not key or not isinstance(key, str):
        return None
    return key
