from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi import HTTPException


app = FastAPI(title="Backend API")

# CORS (frontend ayrı domainde olacağı için gerekli)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # prod'da domain ile sınırlandırılacak
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health_check():
    return {"health": "healthy"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI backend"}

@app.get("/api/lichess/{username}")
def get_lichess_ratings(username: str):
    url = f"https://lichess.org/api/user/{username}"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Lichess API unreachable")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Lichess user not found")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Unexpected Lichess error")

    data = response.json()
    if data.get("disabled") is True or data.get("tosViolation") is True:
        raise HTTPException(
            status_code=404,
            detail="Lichess user not available"
        )

    perfs = data.get("perfs", {})

    return {
        "username": username,
        "ratings": {
            "blitz": perfs.get("blitz", {}).get("rating"),
            "rapid": perfs.get("rapid", {}).get("rating"),
            "bullet": perfs.get("bullet", {}).get("rating"),
        }
    }


