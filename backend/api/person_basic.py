# ==========================================================
# File: backend/api/person_basic.py  (v3.0-PRO-FIX-DATE-AVATAR)
# Mô tả:
#   - Sửa lỗi ngày sinh GMT → ISO yyyy-mm-dd
#   - Avatar chỉ trả về filename (không kèm /static/)
#   - Đồng bộ hoàn hảo với PersonBasicForm v7.2
#   - Không thay đổi logic insert/update/delete
# ==========================================================

from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi import Request
from schemas.person_basic import (
    PersonBasicCreate,
    PersonBasicUpdate,
    RestoreRequest,
    RoleEnum
)
from mysql.connector import Error
from db_helper import get_connection, close_connection
import os
from datetime import datetime

router = APIRouter()


# ==========================================================
# 🔧 CHUYỂN NGÀY MYSQL → ISO yyyy-mm-dd
# ==========================================================
def to_iso(date_value):
    """
    MySQL trả về kiểu datetime hoặc chuỗi GMT như:
        'Sat, 19 May 1956 00:00:00 GMT'
    Hàm này chuyển thành '1956-05-19'
    """
    if not date_value:
        return None

    # Nếu đã là yyyy-mm-dd → OK
    if (
        isinstance(date_value, str)
        and date_value[:4].isdigit()
        and date_value[4] == "-"
    ):
        return date_value[:10]

    try:
        # Parse chuỗi ngày GMT
        dt = datetime.strptime(str(date_value), "%a, %d %b %Y %H:%M:%S GMT")
        return dt.strftime("%Y-%m-%d")
    except:
        pass

    try:
        # datetime object
        return date_value.strftime("%Y-%m-%d")
    except:
        return None


# ==========================================================
# 🔧 AVATAR PATH SAFE (CHỈ TRẢ VỀ FILENAME)
# ==========================================================
def safe_avatar_file(gender, avatar_value, person_id=None):
    """
    Trả về ONLY filename:
        '5.jpg'
        hoặc 'default_male.png'
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(BASE_DIR, "static", "avatars")
    default_map = {
        "male": "default_male.png",
        "female": "default_female.png",
        "other": "default_other.png",
    }

    gen = (gender or "other").lower()
    val = str(avatar_value or "").strip()

    candidates = []

    if val:
        base = os.path.basename(val)
        candidates.append(base)

    if person_id:
        candidates.append(f"{person_id}.jpg")
        candidates.append(f"{person_id}.png")

    candidates.append(default_map.get(gen, "default_other.png"))

    for c in candidates:
        if os.path.exists(os.path.join(static_dir, c)):
            return c

    return default_map.get(gen, "default_other.png")


# ==========================================================
# 🔎 CHECK DUPLICATE
# ==========================================================
@router.post("/api/person/check_duplicate")
async def check_duplicate_person(data: dict = Body(...)):
    conn, cursor = None, None
    try:
        last_name = (data.get("last_name") or "").strip()
        first_name = (data.get("first_name") or "").strip()
        gender = (data.get("gender") or "").strip().lower()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT person_id
            FROM person
            WHERE LOWER(TRIM(REPLACE(last_name,' ',''))) = LOWER(REPLACE(%s,' ','')) 
              AND LOWER(TRIM(REPLACE(first_name,' ',''))) = LOWER(REPLACE(%s,' ','')) 
              AND LOWER(TRIM(gender)) = LOWER(%s)
              AND delete_status = 0
            LIMIT 1
            """,
            (last_name, first_name, gender),
        )

        dup = cursor.fetchone()

        if dup:
            return {"duplicate": True, "message": "⚠️ Thành viên này đã tồn tại!"}

        return {"duplicate": False}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cursor)


# ==========================================================
# 📌 GET LIST — SORT ỔN ĐỊNH
# ==========================================================
@router.get("/api/person/basic")
def get_person_basic_list():
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                person_id,
                sur_name,
                last_name,
                middle_name,                
                first_name,
                gender,
                birth_date,
                death_date,
                avatar
            FROM person
            WHERE delete_status = 0
            ORDER BY
                birth_date IS NULL DESC,
                birth_date ASC,
                first_name ASC
        """
        )

        rows = cursor.fetchall() or []

        for row in rows:
            row["birth_date"] = to_iso(row.get("birth_date"))
            row["death_date"] = to_iso(row.get("death_date"))

            row["avatar"] = safe_avatar_file(
                row.get("gender"), row.get("avatar"), row.get("person_id")
            )

        return rows

    except Error as e:
        print("❌ DROPDOWN SQL ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cursor)


# ==========================================================
# 📌 GET BY ID
# ==========================================================
@router.get("/api/person/basic/{id}")
def get_person_basic_by_id(id):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                p.person_id AS id,
                p.sur_name,
                p.last_name,
                p.middle_name,                
                p.first_name,
                p.gender,
                p.birth_date,
                p.death_date,
                p.avatar,
                MAX(CASE WHEN pc.type = 'FATHER' THEN pc.parent_id END) AS father_id,
                MAX(CASE WHEN pc.type = 'MOTHER' THEN pc.parent_id END) AS mother_id

            FROM person p
            LEFT JOIN parent_child pc ON pc.child_id = p.person_id
            WHERE p.person_id = %s
            GROUP BY p.person_id
        """,
            (id,),
        )

        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Không tìm thấy")

        row["birth_date"] = to_iso(row.get("birth_date"))
        row["death_date"] = to_iso(row.get("death_date"))

        row["avatar"] = safe_avatar_file(row.get("gender"), row.get("avatar"), id)

        return row

    except Error as e:
        print("❌ SQL:", e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cursor)


# ==========================================================
# ➕ ADD PERSON
# ==========================================================
@router.post("/api/person/basic")
async def add_person_basic(data: PersonBasicCreate):
    conn, cursor = None, None
    try:
        role = data.role.value
        if role not in ["member_basic", "member_close", "co_operator", "admin"]:
            raise HTTPException(
                status_code=403, detail="Không có quyền thực hiện thao tác này."
            )

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Duplicate check
        cursor.execute(
            """
            SELECT person_id FROM person
            WHERE LOWER(TRIM(REPLACE(last_name,' ','')))=LOWER(REPLACE(%s,' ','')) 
              AND LOWER(TRIM(REPLACE(first_name,' ','')))=LOWER(REPLACE(%s,' ','')) 
              AND LOWER(TRIM(gender))=LOWER(%s)
              AND delete_status=0
            LIMIT 1
        """,
            (data.last_name, data.first_name, data.gender),
        )

        exists = cursor.fetchone()

        if exists and role in ["member_basic", "member_close"]:
            return JSONResponse(
                status_code=409,
                content={"pending": True, "message": "⚠️ Tồn tại — cần gửi pending."},
            )
        cursor.execute(
            """
            INSERT INTO person (
                sur_name, middle_name, last_name, first_name,
                gender, birth_date, death_date, avatar,
                delete_status, created_at, updated_at
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,0,NOW(),NOW())
        """,
            (
                data.sur_name,
                data.middle_name,
                data.last_name,
                data.first_name,
                data.gender,
                data.birth_date,
                data.death_date,
                data.avatar,
            ),
        )

        conn.commit()

        return JSONResponse(
            status_code=201,
            content={
                "id": cursor.lastrowid,
                "message": "Created"
            }
        )

    except Error as e:
        if conn:
            conn.rollback()
        print("❌ INSERT ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cursor)


# ==========================================================
# ✏️ UPDATE (SAFE PARTIAL UPDATE)
# ==========================================================
@router.put("/api/person/basic/{id}")
async def update_person_basic(id: int, data: PersonBasicUpdate):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Chỉ lấy field được gửi lên
        update_data = data.dict(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="Không có dữ liệu để cập nhật")

        fields = []
        values = []

        for key, value in update_data.items():
            fields.append(f"{key}=%s")
            values.append(value)

        values.append(id)

        sql = f"""
            UPDATE person
            SET {', '.join(fields)}, updated_at=NOW()
            WHERE person_id=%s
        """

        cursor.execute(sql, values)

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy person")

        conn.commit()

        return {"id": id, "message": "Updated"}

    except Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        close_connection(conn, cursor)

# ==========================================================
# 📌 GET FOR PERSON DROPDOWN
# ==========================================================
@router.get("/api/person/for-person-dropdown")
def get_person_for_dropdown():
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                person_id,
                sur_name,
                last_name,
                middle_name,               
                first_name,
                gender,
                birth_date
            FROM person
            WHERE delete_status = 0
            ORDER BY
                birth_date IS NULL DESC,
                birth_date ASC,
                first_name ASC
            """
        )

        rows = cursor.fetchall() or []

        for row in rows:
            row["birth_date"] = to_iso(row.get("birth_date"))

            # Tạo full_name_vn giống frontend đang dùng
            row["full_name_vn"] = " ".join(
                filter(
                    None,
                    [
                        row.get("sur_name"),
                        row.get("last_name"),
                        row.get("middle_name"),
                        row.get("first_name"),
                    ],
                )
            )

        return rows

    except Error as e:
        print("❌ DROPDOWN SQL ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cursor)


# ==========================================================
# 🗑 SOFT DELETE (SAFE)
# ==========================================================
@router.delete("/api/person/basic/{id}")
def delete_person_basic(id: int):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Kiểm tra tồn tại
        cursor.execute(
            "SELECT delete_status FROM person WHERE person_id=%s",
            (id,)
        )
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Không tìm thấy person")

        if row["delete_status"] == 1:
            raise HTTPException(status_code=409, detail="Person đã bị xóa trước đó")

        # Soft delete
        cursor.execute(
            "UPDATE person SET delete_status=1, updated_at=NOW() WHERE person_id=%s",
            (id,)
        )

        conn.commit()

        return {"id": id, "message": "Deleted (soft)"}

    except Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        close_connection(conn, cursor)

# ==========================================================
# ♻️ RESTORE (ROLE CHECK)
# ==========================================================
@router.put("/api/person/basic/{id}/restore")
async def restore_person_basic(id: int, data: RestoreRequest):
    conn, cursor = None, None
    try:
        # Check quyền
        if data.role not in [RoleEnum.co_operator, RoleEnum.admin]:
            raise HTTPException(status_code=403, detail="Không có quyền khôi phục")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Kiểm tra tồn tại
        cursor.execute(
            "SELECT delete_status FROM person WHERE person_id=%s",
            (id,)
        )
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Không tìm thấy person")

        if row["delete_status"] == 0:
            raise HTTPException(status_code=409, detail="Person chưa bị xóa")

        # Restore
        cursor.execute(
            "UPDATE person SET delete_status=0, updated_at=NOW() WHERE person_id=%s",
            (id,)
        )

        conn.commit()

        return {"id": id, "message": "Restored"}

    except Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        close_connection(conn, cursor)


