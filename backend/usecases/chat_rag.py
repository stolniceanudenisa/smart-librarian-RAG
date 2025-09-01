# Main RAG flow orchestration (embed → retrieve → LLM → tool)
from openai import OpenAI
from backend.core.config import settings
from backend.repositories.chroma_repo import ChromaRepository
from backend.tools.book_tools import get_summary_by_title

SYSTEM_PROMPT = (
    "You are a helpful assistant that recommends exactly ONE book from the candidates. "
    "Base your choice only on the short blurbs provided. "
    "Reply with a short rationale and the chosen title."
)

client = OpenAI(api_key=settings.openai_api_key)

def run_chat_rag(user_query: str):
    # 1. Retrieve top-k candidates
    repo = ChromaRepository()
    candidates = repo.query(user_query, top_k=settings.top_k)

    if not candidates:
        return {"title": None, "rationale": "No matches found.", "full_summary": None}

    # 2. Build context for LLM
    context = "\n".join(
        f"- Title: {c['title']}\n  Tags: {', '.join(c['tags'])}\n  Short: {c['short']}"
        for c in candidates
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
        {"role": "assistant", "content": "Candidates:\n" + context}
    ]

    # 3. Let LLM decide
    resp = client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        temperature=0.3,
        max_tokens=200
    )

    rationale = resp.choices[0].message.content.strip()
    # Heuristically extract chosen title (naive: pick first candidate mentioned)
    picked_title = None
    for c in candidates:
        if c["title"].lower() in rationale.lower():
            picked_title = c["title"]
            break
    if not picked_title:
        picked_title = candidates[0]["title"]

    # 4. Deterministic tool call
    try:
        full_summary = get_summary_by_title(picked_title)
    except KeyError:
        full_summary = "(Full summary not found in database.)"

    return {
        "title": picked_title,
        "rationale": rationale,
        "full_summary": full_summary
    }
