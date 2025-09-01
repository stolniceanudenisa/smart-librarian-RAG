import base64
from openai import OpenAI
from backend.core.config import settings

_IMAGE_MODEL = getattr(settings, "image_model", None) or "gpt-image-1"
_DEFAULT_SIZE = "1024x1024"

client = OpenAI(api_key=settings.openai_api_key)

def generate_image_png(prompt: str, size: str | None = None) -> bytes:
    """
    Text → image (PNG). Returns PNG bytes.
    """
    s = size or _DEFAULT_SIZE
    result = client.images.generate(
        model=_IMAGE_MODEL,
        prompt=prompt,
        size=s,
    )
    b64 = result.data[0].b64_json
    return base64.b64decode(b64)
