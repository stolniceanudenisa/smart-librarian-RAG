# profanity filter, rate limiting
BAD_WORDS = ["badword1", "badword2"]

def contains_profanity(text: str) -> bool:
    return any(word in text.lower() for word in BAD_WORDS)
