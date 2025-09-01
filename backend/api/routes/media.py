from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from backend.usecases.generate_tts import synthesize_tts_mp3
from backend.usecases.generate_stt import transcribe_audio
from backend.usecases.generate_image import generate_image_png

router = APIRouter()

# ---- TTS ----
class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=8000)
    voice: str | None = Field(default=None, description="Optional voice name (e.g., alloy)")

@router.post("/tts", response_class=StreamingResponse, summary="Text → Speech (MP3)")
def tts_endpoint(payload: TTSRequest):
    try:
        audio_bytes = synthesize_tts_mp3(payload.text, voice=payload.voice)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {e}")
    headers = {"Content-Disposition": 'inline; filename="speech.mp3"'}
    return StreamingResponse(iter([audio_bytes]), media_type="audio/mpeg", headers=headers)

# ---- STT ----
@router.post("/stt", summary="Speech → Text (Whisper)")
async def stt_endpoint(audio: UploadFile = File(..., description="Audio file (mp3/wav/m4a)")):
    try:
        data = await audio.read()
        text = transcribe_audio(data, filename=audio.filename or "audio.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT error: {e}")
    return {"text": text}

# ---- IMAGE ----
class ImageRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=2000)
    size: str | None = Field(default=None, pattern=r"^\d{3,4}x\d{3,4}$", description="e.g., 512x512, 1024x1024")

@router.post("/image", response_class=StreamingResponse, summary="Text → Image (PNG)")
def image_endpoint(payload: ImageRequest):
    try:
        png_bytes = generate_image_png(prompt=payload.prompt, size=payload.size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation error: {e}")
    headers = {"Content-Disposition": 'inline; filename="image.png"'}
    return StreamingResponse(iter([png_bytes]), media_type="image/png", headers=headers)
