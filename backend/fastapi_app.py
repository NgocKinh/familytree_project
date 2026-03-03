from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="FamilyTree API")

# Static (production safe absolute path)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)
    
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
from api.marriage_fastapi import router as marriage_router
from api.parent_child_fastapi import router as parent_child_router
from api.avatar import router as avatar_router

app.include_router(person_basic_router)
app.include_router(marriage_router)
app.include_router(parent_child_router)
app.include_router(avatar_router)

@app.get("/")
def root():
    return {"message": "FastAPI running"}