# backend/core/guards.py
"""
Guardrails: simple profanity detection & helpers.

- contains_profanity(text) -> bool
- find_profanities(text) -> list[str]
- censor_text(text) -> str
- enforce_profanity_guard(text) -> tuple[bool, str|None]
"""

from __future__ import annotations
import re
import unicodedata
from typing import List, Tuple, Optional
 
BAD_WORDS = {
    "fuck",
    "shit",
    "bitch",
    "asshole",
    "bastard",
    "dick",
    "cunt",
    "motherfucker",
    "slut",
    "whore",
    "piss",
    "cock",
    "prick",
    "douche",
    "twat",
    "wanker",
    "bollocks",
    "arse",
    "jackass",
    "jerkoff",
    "scumbag",
    "hoe",
    "skank",
    "nigger",   # racial slur
    "faggot"    # homophobic slur
}

# Optional whitelist to avoid false positives for substrings.
# Example: "assistant" contains "ass", but we may want to allow "assistant".
SAFE_WHITELIST = {
    "assistant",
    "passage",
    "assign",
}

_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9']+")


def _normalize(text: str) -> str:
    """Lowercase + strip accents for robust matching."""
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text


def _tokenize(text: str) -> List[str]:
    """Simple alnum/apostrophe tokenizer that preserves word boundaries."""
    return _WORD_RE.findall(text)


def contains_profanity(text: str) -> bool:
    """Return True if any token (normalized) matches BAD_WORDS (minus whitelist)."""
    norm = _normalize(text)
    tokens = _tokenize(norm)

    for tok in tokens:
        if tok in BAD_WORDS and tok not in SAFE_WHITELIST:
            return True
    return False


def find_profanities(text: str) -> List[str]:
    """Return the unique profane tokens detected (normalized)."""
    norm = _normalize(text)
    tokens = set(_tokenize(norm))
    return sorted([t for t in tokens if t in BAD_WORDS and t not in SAFE_WHITELIST])


def censor_text(text: str) -> str:
    """
    Naive censor: replace inner letters of detected profane tokens with asterisks.
    Example: 'motherfucker' -> 'm**********r'
    """
    profs = set(find_profanities(text))
    if not profs:
        return text

    # Build a regex for whole-word matches of profanities (case-insensitive, accent-insensitive)
    # We’ll censor *only* exact word matches, not substrings in safe words.
    def accent_insensitive(word: str) -> str:
        # Rough approach: match the normalized letters with a character class that includes
        # common accented variants. For simplicity, just use case-insensitive on raw text;
        # normalization above handles detection; here we rely on token boundaries.
        return r"\b" + re.escape(word) + r"\b"

    pattern = re.compile("|".join(accent_insensitive(w) for w in profs), flags=re.IGNORECASE)

    def repl(m: re.Match) -> str:
        w = m.group(0)
        if len(w) <= 2:
            return "*" * len(w)
        return w[0] + ("*" * (len(w) - 2)) + w[-1]

    return pattern.sub(repl, text)


def enforce_profanity_guard(text: str) -> Tuple[bool, Optional[str]]:
    """
    Returns (is_blocked, message).
    - If profanity detected → (True, polite_message)
    - Else → (False, None)
    """
    if contains_profanity(text):
        bad = ", ".join(find_profanities(text))
        msg = (
            "Your message contains inappropriate language "
            f"({bad}). Please rephrase and try again."
        )
        return True, msg
    return False, None
