# ============================================================
# NOTE:
#   File này CHỈ xử lý CRUD + query cho bảng person.
#   - Không chứa logic suy luận quan hệ gia đình.
#   - Mọi quan hệ cha/con, anh/em được xử lý ở layer khác.
# ============================================================

from flask import Blueprint, request, jsonify
from mysql.connector import Error
from db import get_connection

person_bp = Blueprint("person_bp", __name__)

# ======================================================================
# 🔹 GET ALL PERSONS — hỗ trợ lọc bằng query param
#    /api/person?status=active | hidden | all
# ======================================================================
@person_bp.route("/api/person/", methods=["GET"])
def get_all_persons():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        status = request.args.get("status", "all")

        where_clause = ""
        if status == "active":
            where_clause = "WHERE delete_status = 0"
        elif status == "hidden":
            where_clause = "WHERE delete_status = 1"

        sql = f"""
            SELECT 
                person_id,
                sur_name,
                last_name,
                middle_name,
                first_name,
                gender,
                birth_date,
                death_date,
                delete_status,
                full_name_vn
            FROM person
            {where_clause}
            ORDER BY 
                CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END ASC,
                birth_date DESC,
                first_name ASC
        """

        cur.execute(sql)
        rows = cur.fetchall()
        return jsonify(rows), 200

    except Exception as e:
        print("🔥 ERROR /api/person:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# ============================================================
# 🔹 GET PERSONS FOR CHILD DROPDOWN
#     - chỉ ACTIVE (delete_status = 0)
#     - sort đúng nghiệp vụ chọn CON
# ============================================================
@person_bp.route("/api/person/for-person-dropdown", methods=["GET"])
def get_persons_for_person_dropdown():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        sql = """
            SELECT
                person_id,
                full_name_vn,
                gender,
                birth_date,
                first_name
            FROM person
            WHERE delete_status = 0
            ORDER BY
                CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END,
                birth_date DESC,
                first_name ASC
        """

        cur.execute(sql)
        rows = cur.fetchall()
        return jsonify(rows), 200

    except Exception as e:
        print("🔥 ERROR /api/person/for-person-dropdown:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# ============================================================
# GET ONE PERSON — giữ nguyên
# ============================================================
@person_bp.route("/api/person/<int:person_id>", methods=["GET"])
def get_person(person_id):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM person WHERE person_id = %s", (person_id,))
        row = cursor.fetchone()

        if row:
            return jsonify(row), 200
        return jsonify({"error": "Person not found"}), 404

    except Error as e:
        print("❌ Lỗi SQL:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ============================================================
# POST create person — giữ nguyên
# ============================================================
@person_bp.route("/api/person/", methods=["POST"])
def create_person():
    conn, cursor = None, None
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO person (
                sur_name, last_name, middle_name, first_name, gender,
                birth_date, birth_date_precision,
                death_date, death_date_precision,
                delete_status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 0)
        """

        vals = (
            data.get("sur_name"),
            data.get("last_name"),
            data.get("middle_name"),
            data.get("first_name"),
            data.get("gender"),
            data.get("birth_date"),
            data.get("birth_date_precision"),
            data.get("death_date"),
            data.get("death_date_precision"),
        )

        cursor.execute(sql, vals)
        conn.commit()

        return jsonify({
            "message": "Person created",
            "person_id": cursor.lastrowid
        }), 201

    except Error as e:
        print("❌ Lỗi SQL:", e)
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ============================================================
# PUT update person — giữ nguyên
# ============================================================
@person_bp.route("/api/person/<int:person_id>", methods=["PUT"])
def update_person(person_id):
    conn, cursor = None, None
    data = request.json

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE person
            SET sur_name=%s, last_name=%s, middle_name=%s, first_name=%s,
                gender=%s, birth_date=%s, birth_date_precision=%s,
                death_date=%s, death_date_precision=%s,
                updated_at=NOW()
            WHERE person_id=%s
        """

        vals = (
            data.get("sur_name"),
            data.get("last_name"),
            data.get("middle_name"),
            data.get("first_name"),
            data.get("gender"),
            data.get("birth_date"),
            data.get("birth_date_precision"),
            person_id,
        )

        cursor.execute(sql, vals)
        conn.commit()

        return jsonify({"message": "Person updated"}), 200

    except Error as e:
        print("❌ Lỗi SQL:", e)
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ============================================================
# DELETE soft — giữ nguyên
# ============================================================
@person_bp.route("/api/person/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    conn, cursor = None, None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE person
            SET delete_status = 1, deleted_at = NOW()
            WHERE person_id = %s
        """

        cursor.execute(sql, (person_id,))
        conn.commit()

        return jsonify({"message": "Person deleted"}), 200

    except Error as e:
        print("❌ Lỗi SQL:", e)
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
