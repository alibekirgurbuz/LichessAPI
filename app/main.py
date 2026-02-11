from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Backend API")

# CORS (frontend ayrı domainde olacağı için gerekli)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # prod'da domain ile sınırlandırılacak
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
this_will_break =

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health_check():
    return {"health": "healthy"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI backend"}
