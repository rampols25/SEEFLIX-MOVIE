from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="See-Flix Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This backend is intentionally an adapter. Keep private provider credentials here,
# never in the GitHub frontend. Only return media you are authorized to serve.

CATALOG = {
    "movies": [],
    "tv": [],
    "cdrama": [],
    "anime": [],
}

class PlayRequest(BaseModel):
    id: str | int
    type: str
    season: int | None = None
    episode: int | None = None

@app.get("/")
def root():
    return {"status": "See-Flix backend online"}

@app.get("/api/search")
def search(q: str = Query(..., min_length=2)):
    q = q.lower().strip()
    results = []
    for group in CATALOG.values():
        for item in group:
            title = (item.get("title") or item.get("name") or "").lower()
            if q in title:
                results.append(item)
    return {"query": q, "results": results[:40]}

@app.get("/api/trending/{category}")
def trending(category: str):
    if category not in CATALOG:
        raise HTTPException(404, "Unknown category")
    return {"results": CATALOG[category]}

@app.get("/api/item/{item_type}/{item_id}")
def item(item_type: str, item_id: str):
    for entry in CATALOG.get("movies" if item_type == "movie" else "tv", []):
        if str(entry.get("id")) == str(item_id):
            return entry
    raise HTTPException(404, "Title not found")

@app.get("/api/tv/{tv_id}/seasons")
def seasons(tv_id: str):
    # Populate this from your authorized catalog/provider.
    return {"seasons": []}

@app.get("/api/tv/{tv_id}/season/{season_number}")
def episodes(tv_id: str, season_number: int):
    # Populate this from your authorized catalog/provider.
    return {"episodes": []}

@app.post("/api/play")
def play(req: PlayRequest):
    # IMPORTANT:
    # Replace this with a URL from media you are legally authorized to stream.
    # Do not put third-party/private provider credentials in the frontend.
    raise HTTPException(
        501,
        "No authorized playback source configured. Add your licensed media URL resolver here."
    )
