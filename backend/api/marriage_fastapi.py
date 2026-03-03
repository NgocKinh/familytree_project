# ==========================================================
# File: backend/api/marriage_fastapi.py
# Port từ Flask → FastAPI (STEP 1: GET ALL)
# ==========================================================

from fastapi import APIRouter, HTTPException
from db_helper import get_connection, close_connection
from fastapi.responses import JSONResponse
from fastapi import status
from schemas.marriage import MarriageCreate
from services.consanguinity import are_related
router = APIRouter()


def build_name_raw(p):
    return f"{p.get('last_name','')}|{p.get('middle_name','')}|{p.get('first_name','')}"


# ==========================================================
# 🔹 GET ALL
# ==========================================================
@router.get("/api/marriage")
def get_all_marriages():
    conn, cur = None, None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            """
            SELECT 
                m.id,
                m.spouse_a_id, 
                p1.sur_name AS spouse_a_sur,
                p1.last_name AS a_last, p1.middle_name AS a_mid, p1.first_name AS a_first,
                m.spouse_b_id,
                p2.sur_name AS spouse_b_sur,
                p2.last_name AS b_last, p2.middle_name AS b_mid, p2.first_name AS b_first,
                m.start_date, m.end_date,
                m.status, m.ceremony_type, m.location,
                m.notes, m.consanguineous
            FROM marriage m
            JOIN person p1 ON p1.person_id = m.spouse_a_id AND p1.delete_status = 0
            JOIN person p2 ON p2.person_id = m.spouse_b_id AND p2.delete_status = 0
            ORDER BY m.id ASC
        """
        )

        rows = cur.fetchall() or []

        for r in rows:
            r["spouse_a_name"] = build_name_raw(
                {
                    "last_name": r["a_last"],
                    "middle_name": r["a_mid"],
                    "first_name": r["a_first"],
                }
            )
            r["spouse_b_name"] = build_name_raw(
                {
                    "last_name": r["b_last"],
                    "middle_name": r["b_mid"],
                    "first_name": r["b_first"],
                }
            )

        return rows

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cur)


# ==========================================================
# 🔹 POST CREATE
# ==========================================================
@router.post("/api/marriage", status_code=status.HTTP_201_CREATED)
def create_marriage(payload: MarriageCreate):
    conn, cur = None, None
    try:
        spouse_a_id = payload.spouse_a_id
        spouse_b_id = payload.spouse_b_id
        start_date = payload.start_date
        end_date = payload.end_date
        status = payload.status
        ceremony_type = payload.ceremony_type
        location = payload.location
        notes = payload.notes
        consanguineous = int(payload.consanguineous or 0)
        
        if spouse_a_id == spouse_b_id:
            raise HTTPException(status_code=409, detail="Spouses cannot be the same person")
        # Chuẩn hóa thứ tự ID
        if spouse_a_id > spouse_b_id:
            spouse_a_id, spouse_b_id = spouse_b_id, spouse_a_id
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        # Kiểm tra 2 person tồn tại và chưa bị xóa
        cur.execute("""
            SELECT person_id FROM person
            WHERE person_id IN (%s, %s)
            AND delete_status = 0
        """, (spouse_a_id, spouse_b_id))

        persons = cur.fetchall()

        if len(persons) != 2:
            raise HTTPException(status_code=404, detail="One or both persons not found")
        
        cur.execute("""
            SELECT id FROM marriage
            WHERE (spouse_a_id = %s AND spouse_b_id = %s)
            OR (spouse_a_id = %s AND spouse_b_id = %s)
        """, (spouse_a_id, spouse_b_id, spouse_b_id, spouse_a_id))

        if cur.fetchone():
            raise HTTPException(status_code=409, detail="Marriage already exists")
        # 🔎 Kiểm tra huyết thống
        related = are_related(conn, spouse_a_id, spouse_b_id)

        if related and not consanguineous:
            raise HTTPException(
                status_code=409,
                detail="⚠ Hai người có quan hệ huyết thống. Click vào ô 'Cùng Huyết Thống' để chấp nhận mối quan hệ này"
            )
        # 🔥 Chuẩn hóa ceremony_type để tránh ENUM lỗi 1265
        if not ceremony_type:
            ceremony_type = None
        cur.execute(
            """
            INSERT INTO marriage (
                spouse_a_id,
                spouse_b_id,
                start_date,
                end_date,
                status,
                ceremony_type,
                location,
                notes,
                consanguineous
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
            (
                spouse_a_id,
                spouse_b_id,
                start_date,
                end_date,
                status,
                ceremony_type,
                location,
                notes,
                consanguineous,
            ),
        )

        conn.commit()

        return {"id": cur.lastrowid, "message": "Created"}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        import traceback
        traceback.print_exc()
        print("🔥 MARRIAGE ERROR:", e)
        if "1062" in str(e):
            raise HTTPException(status_code=409, detail="Duplicate marriage relation")

        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cur)

# ==========================================================
# 🔹 GET ONE
# ==========================================================
@router.get("/api/marriage/{mid}")
def get_marriage(mid: int):
    conn, cur = None, None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM marriage WHERE id=%s", (mid,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Marriage not found")

        return row

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cur)


# ==========================================================
# 🔹 UPDATE
# ==========================================================
@router.put("/api/marriage/{mid}")
def update_marriage(mid: int, payload: dict):
    conn, cur = None, None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT id FROM marriage WHERE id=%s", (mid,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Marriage not found")
        spouse_a_id = payload.get("spouse_a_id")
        spouse_b_id = payload.get("spouse_b_id")
        consanguineous = int(payload.get("consanguineous") or 0)

        related = are_related(conn, spouse_a_id, spouse_b_id)

        if related and not consanguineous:
            raise HTTPException(
                status_code=409,
                detail="⚠ Hai người có quan hệ huyết thống (≤ 5 đời). Hãy tick 'Cùng huyết thống' để xác nhận."
            )
        cur.execute(
            """
            UPDATE marriage SET
                spouse_a_id=%s,
                spouse_b_id=%s,
                start_date=%s,
                end_date=%s,
                status=%s,
                ceremony_type=%s,
                location=%s,
                notes=%s,
                consanguineous=%s
            WHERE id=%s
        """,
            (
                payload.get("spouse_a_id"),
                payload.get("spouse_b_id"),
                payload.get("start_date"),
                payload.get("end_date"),
                payload.get("status"),
                payload.get("ceremony_type"),
                payload.get("location"),
                payload.get("notes"),
                payload.get("consanguineous", 0),
                mid,
            ),
        )

        conn.commit()
        return {"message": "updated"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cur)


# ==========================================================
# 🔹 DELETE
# ==========================================================
@router.delete("/api/marriage/{mid}")
def delete_marriage(mid: int):
    conn, cur = None, None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM marriage WHERE id=%s", (mid,))
        conn.commit()

        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Marriage not found")

        return {"message": "Deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cur)
