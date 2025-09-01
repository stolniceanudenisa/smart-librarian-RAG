from openai import OpenAI
from backend.core.config import settings

# default whisper model
_STT_MODEL = getattr(settings, "stt_model", None) or "whisper-1"

client = OpenAI(api_key=settings.openai_api_key)

def transcribe_audio(file_bytes: bytes, filename: str = "audio.wav") -> str:
    """
    Speech → text. Accepts raw audio bytes (mp3/wav/m4a), returns transcript.
    """
    transcription = client.audio.transcriptions.create(
        model=_STT_MODEL,
        file=(filename, file_bytes),
    )
    return transcription.text
