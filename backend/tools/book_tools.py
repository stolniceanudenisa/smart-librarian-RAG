# get_summary_by_title, condense_summary
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

DATA_PATH = Path("data/book_summaries.json")
_BOOKS_CACHE: Optional[Dict[str, Dict[str, Any]]] = None

def _load_books() -> Dict[str, Dict[str, Any]]:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return {entry["title"]: entry for entry in data}

def get_summary_by_title(title: str) -> str:
    global _BOOKS_CACHE
    if _BOOKS_CACHE is None:
        _BOOKS_CACHE = _load_books()
    book = _BOOKS_CACHE.get(title)
    if not book:
        raise KeyError(f"Title not found: {title}")
    return book["full"]

def get_short_records_for_ingest() -> List[Tuple[str, str, Dict[str, Any]]]:
    """
    Returns a list of (id, document, metadata) tuples for Chroma upsert.
      id        = slugified title
      document  = short blurb (3–5 lines)
      metadata  = {"title": str, "tags": list[str]}
    """
    global _BOOKS_CACHE
    if _BOOKS_CACHE is None:
        _BOOKS_CACHE = _load_books()

    def slug(title: str) -> str:
        return "".join(ch.lower() if ch.isalnum() else "-" for ch in title).strip("-")

    rows: List[Tuple[str, str, Dict[str, Any]]] = []
    for title, rec in _BOOKS_CACHE.items():
        rows.append(
            (slug(title), rec["short"], {"title": title, "tags": rec.get("tags", [])})
        )
    return rows
