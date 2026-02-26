from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="FamilyTree API")

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
ENV = os.environ.get("FLASK_ENV", "development")

if ENV == "development":
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
else:
    origins = ["https://familytree.example.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# REGISTER ROUTERS
# ==============================
from api.person_basic import router as person_basic_router

app.include_router(person_basic_router)

@app.get("/")
def root():
    return {"message": "FastAPI running"}