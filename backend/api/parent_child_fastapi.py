# ==========================================================
# File: backend/api/parent_child_fastapi.py
# Port từ Flask → FastAPI
# ==========================================================

from fastapi import APIRouter, HTTPException
from db_helper import get_connection, close_connection
from api.gene_propagate import safe_propagate
from utils.blood_utils import update_blood_code

router = APIRouter()


# ==========================================================
# 🔹 GET ALL
# ==========================================================
@router.get("/api/parent_child")
def get_all_parent_child():
    conn, cur = None, None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT 
                pc.id,
                pc.parent_id,
                p1.full_name_vn AS parent_name,
                pc.child_id,
                p2.full_name_vn AS child_name,
                pc.type,
                pc.notes
            FROM parent_child pc
            JOIN person p1 ON pc.parent_id = p1.person_id AND p1.delete_status = 0
            JOIN person p2 ON pc.child_id = p2.person_id AND p2.delete_status = 0
            ORDER BY pc.id ASC
        """)

        rows = cur.fetchall() or []
        return rows

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cur)

# ==========================================================
# 🔹 GET ONE
# ==========================================================
@router.get("/api/parent_child/{rid}")
def get_one_parent_child(rid: int):
    conn, cur = None, None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT 
                pc.id,
                pc.parent_id,
                p1.full_name_vn AS parent_name,
                pc.child_id,
                p2.full_name_vn AS child_name,
                pc.type,
                pc.notes
            FROM parent_child pc
            JOIN person p1 ON pc.parent_id = p1.person_id AND p1.delete_status = 0
            JOIN person p2 ON pc.child_id = p2.person_id AND p2.delete_status = 0
            WHERE pc.id = %s
        """, (rid,))

        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Relation not found")

        return row

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cur)

# ==========================================================
# 🔹 GET CHILD PARENTS STATUS
# ==========================================================
@router.get("/api/child/{child_id}/parents-status")
def get_child_parents_status(child_id: int):
    conn, cur = None, None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT type
            FROM parent_child
            WHERE child_id = %s
        """, (child_id,))

        rows = cur.fetchall() or []

        has_father = any(r["type"] == "FATHER" for r in rows)
        has_mother = any(r["type"] == "MOTHER" for r in rows)

        return {
            "has_father": has_father,
            "has_mother": has_mother
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cur)

# ==========================================================
# 🔹 ASSIGN PARENT (CLEAN WRITE)
# ==========================================================
@router.post("/api/parent_child/assign", status_code=201)
def assign_parent_clean(payload: dict):
    conn, cur = None, None
    try:
        child_id = payload.get("child_id")
        parent_id = payload.get("parent_id")
        ptype = payload.get("type")

        if ptype not in ("FATHER", "MOTHER"):
            raise HTTPException(status_code=400, detail="Invalid parent type")

        if child_id == parent_id:
            raise HTTPException(status_code=400, detail="Parent and child cannot be the same")

        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        # 1️⃣ Check child tồn tại
        cur.execute("""
            SELECT 1 FROM person
            WHERE person_id = %s AND delete_status = 0
        """, (child_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Child not found")

        # 2️⃣ Check parent tồn tại + gender
        cur.execute("""
            SELECT gender FROM person
            WHERE person_id = %s AND delete_status = 0
        """, (parent_id,))
        parent = cur.fetchone()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")

        gender = parent["gender"]
        if ptype == "FATHER" and gender != "MALE":
            raise HTTPException(status_code=400, detail="Father must be male")
        if ptype == "MOTHER" and gender != "FEMALE":
            raise HTTPException(status_code=400, detail="Mother must be female")

        # 3️⃣ Không cho trùng cha/mẹ
        cur.execute("""
            SELECT 1 FROM parent_child
            WHERE child_id = %s AND type = %s
        """, (child_id, ptype))
        if cur.fetchone():
            raise HTTPException(
                status_code=400,
                detail=f"Child already has a {ptype.lower()}"
            )

        # 4️⃣ Insert 1 lần duy nhất
        cur.execute("""
            INSERT INTO parent_child (parent_id, child_id, type)
            VALUES (%s, %s, %s)
        """, (parent_id, child_id, ptype))

        # 5️⃣ Propagate (trong transaction)
        safe_propagate(
            conn=conn,
            old_id=None,
            new_id=parent_id,
            side=ptype,
            executor="system"
        )

        update_blood_code(
            conn=conn,
            child_id=child_id
        )

        # 6️⃣ Commit
        conn.commit()

        return {"message": "Parent assigned successfully"}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()

        if "1062" in str(e):
            raise HTTPException(status_code=409, detail="Parent already assigned")

        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(conn, cur)
