from fastapi import FastAPI
from app.core.relationship_resolver import RelationshipResolver
from fastapi.middleware.cors import CORSMiddleware
from api.marriage_fastapi import router as marriage_router
from api.person_basic import router as person_router
import logging

# Cấu hình logging toàn hệ thống
logging.basicConfig(
    level=logging.INFO,  # đổi DEBUG khi cần debug
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(person_router)
app.include_router(marriage_router)
# Tạo resolver 1 lần (không tạo mỗi request)
resolver = RelationshipResolver()


@app.get("/relationship")
def get_relationship(source_id: int, target_id: int):
    return resolver.resolve(source_id, target_id)

