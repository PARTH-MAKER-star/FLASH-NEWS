import json
import httpx
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# ----------------------------------------------------------
# 🔑 Replace this with your actual Twitter API Bearer Token
# ----------------------------------------------------------
BEARER_TOKEN = "YOUR_TWITTER_BEARER_TOKEN"
TWITTER_STREAM_URL = "https://api.twitter.com/2/tweets/search/stream"

app = FastAPI()

# Allow dashboard or any frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Stream tweets in realtime ----
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
    return {"message": "✅ Fast Twitter Stream is running!"}
