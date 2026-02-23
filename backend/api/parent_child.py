from flask import Blueprint, request, jsonify
from db import get_connection
from api.gene_propagate import safe_propagate  # ✅ Giữ nguyên phần propagate gene
from utils.blood_utils import update_blood_code  # ✅ Thêm dòng import mới


parent_child_bp = Blueprint("parent_child_bp", __name__)


# ================================================================
# 🔹 GET ALL: Lấy toàn bộ quan hệ cha/mẹ–con
# ================================================================
@parent_child_bp.route(
    "/api/parent_child", methods=["GET"], endpoint="parent_child_get_all"
)
def get_all_parent_child():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT 
                pc.id,
                pc.parent_id,
                p1.full_name_vn AS parent_name,
                pc.child_id,
                p2.full_name_vn AS child_name,
                pc.type,
                pc.notes
            FROM parent_child pc
            JOIN person p1 ON pc.parent_id = p1.person_id AND p1.delete_status = 0   -- ✅ [CHANGE 1]
            JOIN person p2 ON pc.child_id = p2.person_id AND p2.delete_status = 0   -- ✅ [CHANGE 2]
            ORDER BY pc.id ASC
        """
        )
        rows = cur.fetchall()

        return jsonify(rows), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


# ================================================================
# 🔹 GET ONE: Lấy 1 quan hệ theo ID
# ================================================================
@parent_child_bp.route(
    "/api/parent_child/<int:rid>", methods=["GET"], endpoint="parent_child_get_one"
)
def get_one_parent_child():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
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
        """
        )
        rows = cur.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


@parent_child_bp.route("/api/child/<int:child_id>/parents-status", methods=["GET"])
def get_child_parents_status(child_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT type
        FROM parent_child
        WHERE child_id = %s
    """,
        (child_id,),
    )

    rows = cursor.fetchall()

    has_father = any(r["type"] == "FATHER" for r in rows)
    has_mother = any(r["type"] == "MOTHER" for r in rows)

    return {"has_father": has_father, "has_mother": has_mother}

# ================================================================
# ✅ CLEAN WRITE: GHI CHA / MẸ (HỆ MÁU)
# ================================================================
@parent_child_bp.route("/api/parent_child/assign", methods=["POST"])
def assign_parent_clean():
    data = request.json
    child_id = data.get("child_id")
    parent_id = data.get("parent_id")
    ptype = data.get("type")  # FATHER | MOTHER

    if ptype not in ("FATHER", "MOTHER"):
        return jsonify({"error": "Invalid parent type"}), 400

    if child_id == parent_id:
        return jsonify({"error": "Parent and child cannot be the same"}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        # 1️⃣ Không cho trùng cha hoặc mẹ
        cur.execute(
            """
            SELECT 1 FROM parent_child
            WHERE child_id = %s AND type = %s
            """,
            (child_id, ptype),
        )
        if cur.fetchone():
            return jsonify({"error": f"Child already has a {ptype.lower()}"}), 400

        # 2️⃣ Ghi quan hệ
        cur.execute(
            """
            INSERT INTO parent_child (parent_id, child_id, type)
            VALUES (%s, %s, %s)
            """,
            (parent_id, child_id, ptype),
        )
        conn.commit()

        # 3️⃣ Giữ nguyên logic cũ (nếu hệ bạn đang dùng)
        safe_propagate(parent_id, child_id)
        update_blood_code(child_id)

        return jsonify({"message": "Parent assigned successfully"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()

# ================================================================
# 🔒 BLOCK WRITE: KHÓA GHI QUAN HỆ CHA–CON (CLEAN V1)
# ================================================================
@parent_child_bp.route("/api/parent_child", methods=["POST", "PUT", "DELETE"])
def block_parent_child_write():
    return (
        jsonify({"error": "Direct write to parent_child is disabled. Use CLEAN API."}),
        403,
    )
# ================================================================
# 🔍 READ CORE: LẤY CHA / MẸ CỦA 1 PERSON (KHÔNG PHẢI API)
# ⚠️ CORE READ FUNCTION
# - TẤT CẢ suy luận quan hệ (anh em, ông bà…) PHẢI đọc qua hàm này
# - KHÔNG đọc trực tiếp bảng parent_child ở nơi khác
# - KHÔNG suy luận tại đây
# ================================================================
def parents_of(child_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    father_id = None
    mother_id = None

    try:
        cur.execute(
            """
            SELECT parent_id, type
            FROM parent_child
            WHERE child_id = %s
            """,
            (child_id,),
        )

        rows = cur.fetchall()
        for r in rows:
            if r["type"] == "FATHER":
                father_id = r["parent_id"]
            elif r["type"] == "MOTHER":
                mother_id = r["parent_id"]

        return {
            "father_id": father_id,
            "mother_id": mother_id,
        }

    finally:
        cur.close()
        conn.close()
