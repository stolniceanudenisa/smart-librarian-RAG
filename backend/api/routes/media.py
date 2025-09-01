from fastapi import APIRouter

router = APIRouter()

@router.post("/tts")
def tts_endpoint():
    # TODO: implement TTS
    return {"message": "tts placeholder"}

@router.post("/stt")
def stt_endpoint():
    # TODO: implement STT
    return {"message": "stt placeholder"}

@router.post("/image")
def image_endpoint():
    # TODO: implement image generation
    return {"message": "image placeholder"}
