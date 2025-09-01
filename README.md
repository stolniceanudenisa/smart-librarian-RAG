# Smart Librarian – AI with RAG + Tool

Smart Librarian is an AI chatbot that recommends books based on user interests.
It uses Retrieval-Augmented Generation (RAG) with OpenAI GPT and ChromaDB:

- ChromaDB stores short blurbs of books (for semantic search).

- OpenAI GPT selects the best match from candidates.

- Tooling layer (get_summary_by_title) appends the deterministic full summary from local JSON.


Features

- Recommend one book per query

- Retrieve candidates using embeddings + ChromaDB

- Deterministic full summaries (no hallucinations)

- Swagger UI for easy testing

- Guardrails (profanity filter, rate limiting – WIP)

- Text-to-Speech (TTS) endpoint to listen to recommendations

- Speech-to-Text (STT) endpoint to send voice queries

- Image generation endpoint to create book covers or scenes



# 🛠️ Setup Instructions

## 1. Clone and enter project
```
git clone https://github.com/yourusername/smart-librarian-RAG.git
cd smart-librarian-RAG
```

## 2. Create virtual environment
```
python -m venv venv
# Activate venv
# Linux/Mac:
source venv/bin/activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
```


## 3. Install dependencies
```
pip install -r requirements.txt
```

## 4. Set up environment variables
```
Create a file named .env in the project root:

OPENAI_API_KEY=sk-your-key-here
CHROMA_DB_DIR=./chroma
EMBED_MODEL=text-embedding-3-small
CHROMA_COLLECTION=books
TOP_K=5
OPENAI_MODEL=gpt-4o-mini
```


## 5. Add your book summaries
```
Edit data/book_summaries.json and include at least 10 books:

[
  {
    "title": "1984",
    "tags": ["dystopia", "freedom", "control"],
    "short": "A dystopian story about a totalitarian society controlled by Big Brother.",
    "full": "George Orwell's novel depicts a dystopian society under total state control..."
  }
]
```


## ▶️ Running the App
Start FastAPI server
```
uvicorn backend.main:app --reload


Server runs at: http://127.0.0.1:8000

Swagger UI docs: http://127.0.0.1:8000/docs
```


## Ingest books into Chroma
```
Run once after editing your book_summaries.json:

curl -X POST http://127.0.0.1:8000/ingest/
```



## Expected response:
```
{"status":"ok","ingested":10,"collection":"books","persist_dir":"./chroma"}
```



## Test chat
```
Go to Swagger UI → POST /chat and send:

{ "query": "I want a book about friendship and magic" }
```


## Example response:
```
{
  "title": "The Hobbit",
  "rationale": "I recommend The Hobbit because it emphasizes friendship and adventure with magical themes.",
  "full_summary": "Bilbo Baggins, a comfort-loving hobbit..."
}
```
 



 
# 🔒 Guardrails

The app includes a profanity filter that checks user queries before they are sent to the language model.  

If inappropriate language is detected, the request is blocked and the user is asked to rephrase.  

You can extend the bad-words list to cover English or other languages as needed.

 


# 🎙️🎧🖼️ Media Endpoints

These are grouped under /media and are ready to use in Swagger.



# Text → Speech (TTS)
```
Converts text to an MP3 stream.

Endpoint
POST /media/tts


Body
{ "text": "Hello from Smart Librarian!", "voice": "alloy" }

Returns
audio/mpeg (MP3 bytes)
```


# Speech → Text (STT)
```
Uploads an audio file (mp3/wav/m4a) and returns transcription.

Endpoint
POST /media/stt


Form-data
Field name: audio
File: your mp3 / wav / m4a

Returns
{ "text": "..." }
```



# Text → Image
```
Generates a PNG image from a prompt.

Endpoint
POST /media/image


Body
{ "prompt": "a cozy reading nook with warm light and vintage books", "size": "1024x1024" }


Returns

image/png (PNG bytes)
```