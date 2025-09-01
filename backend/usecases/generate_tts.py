from openai import OpenAI
from backend.core.config import settings

# use gpt-4o-mini-tts by default; if not enabled on your account, try "tts-1"
_TTS_MODEL = getattr(settings, "tts_model", None) or "gpt-4o-mini-tts"
_DEFAULT_VOICE = "alloy"

client = OpenAI(api_key=settings.openai_api_key)

def synthesize_tts_mp3(text: str, voice: str | None = None) -> bytes:
    """
    Text → speech (MP3). Returns raw bytes.
    """
    v = voice or _DEFAULT_VOICE
    resp = client.audio.speech.create(
        model=_TTS_MODEL,
        voice=v,
        input=text,
        format="mp3",
    )
    return resp.read()
