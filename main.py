import json
import httpx
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# Replace with your actual Twitter API token
BEARER_TOKEN = "1985961754921209856kh57977185"
TWITTER_STREAM_URL = "https://api.twitter.com/2/tweets/search/stream"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_twitter_stream():
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("GET", TWITTER_STREAM_URL, headers=headers) as response:
            async for line in response.aiter_lines():
                if line:
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async for tweet in get_twitter_stream():
        await websocket.send_text(json.dumps(tweet))

@app.get("/")
def root():
    return {"message": "⚡ FLASH NEWS backend is live!"}
