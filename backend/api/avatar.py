# ==========================================================
# File: backend/api/avatar.py
# Avatar V5 — Production Hardened
# ==========================================================

from fastapi import APIRouter, UploadFile, File, HTTPException
from db_helper import get_connection, close_connection
import os
import uuid

router = APIRouter()

# ==========================================================
# CONFIG
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_DIR = os.path.join(BASE_DIR, "static", "avatars")

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
ALLOWED_MIME = {"image/jpeg": ".jpg", "image/png": ".png"}

os.makedirs(AVATAR_DIR, exist_ok=True)


# ==========================================================
# 📌 UPLOAD AVATAR
# ==========================================================
@router.post("/api/person/{person_id}/avatar")
async def upload_avatar(person_id: int, file: UploadFile = File(...)):

    # 1️⃣ MIME CHECK
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận JPG hoặc PNG")

    # 2️⃣ SIZE LIMIT
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File vượt quá 2MB")

    # reset pointer
    await file.seek(0)

    # 3️⃣ CHECK PERSON EXISTS
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT person_id FROM person WHERE person_id=%s AND delete_status=0",
            (person_id,),
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy person")
    finally:
        close_connection(conn, cursor)

    # 4️⃣ HASH RENAME (cache busting auto)
    ext = ALLOWED_MIME[file.content_type]
    unique_id = uuid.uuid4().hex[:8]
    filename = f"{person_id}_{unique_id}{ext}"
    file_path = os.path.join(AVATAR_DIR, filename)

    # 5️⃣ SAVE FILE
    with open(file_path, "wb") as f:
        f.write(contents)

    # 6️⃣ REMOVE OLD AVATAR (overwrite safe)
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT avatar FROM person WHERE person_id=%s",
            (person_id,),
        )
        row = cursor.fetchone()

        if row and row.get("avatar"):
            old_file = os.path.join(AVATAR_DIR, row["avatar"])
            if os.path.exists(old_file):
                try:
                    os.remove(old_file)
                except Exception:
                    pass

        # 7️⃣ UPDATE DB (save filename only)
        cursor.execute(
            "UPDATE person SET avatar=%s, updated_at=NOW() WHERE person_id=%s",
            (filename, person_id),
        )
        conn.commit()

    finally:
        close_connection(conn, cursor)

    return {
        "message": "Avatar uploaded successfully",
        "filename": filename
    }