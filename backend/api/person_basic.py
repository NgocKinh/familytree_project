# ==========================================================
# File: backend/api/person_basic.py  (v3.0-PRO-FIX-DATE-AVATAR)
# Mô tả:
#   - Sửa lỗi ngày sinh GMT → ISO yyyy-mm-dd
#   - Avatar chỉ trả về filename (không kèm /static/)
#   - Đồng bộ hoàn hảo với PersonBasicForm v7.2
#   - Không thay đổi logic insert/update/delete
# ==========================================================

from flask import Blueprint, jsonify, request
from mysql.connector import Error
from db_helper import get_connection, close_connection
import os
from datetime import datetime

person_basic_bp = Blueprint("person_basic", __name__)

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
    if isinstance(date_value, str) and date_value[:4].isdigit() and date_value[4] == "-":
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
    static_dir = os.path.abspath(os.path.join("backend", "static", "avatars"))

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
@person_basic_bp.route("/api/person/check_duplicate", methods=["POST"])
def check_duplicate_person():
    conn, cursor = None, None
    try:
        data = request.get_json() or {}
        last_name = (data.get("last_name") or "").strip()
        first_name = (data.get("first_name") or "").strip()
        gender = (data.get("gender") or "").strip().lower()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT person_id
            FROM person
            WHERE LOWER(TRIM(REPLACE(last_name,' ',''))) = LOWER(REPLACE(%s,' ','')) 
              AND LOWER(TRIM(REPLACE(first_name,' ',''))) = LOWER(REPLACE(%s,' ','')) 
              AND LOWER(TRIM(gender)) = LOWER(%s)
              AND delete_status = 0
            LIMIT 1
        """, (last_name, first_name, gender))

        dup = cursor.fetchone()

        if dup:
            return jsonify({
                "duplicate": True,
                "message": "⚠️ Thành viên này đã tồn tại!"
            }), 200

        return jsonify({"duplicate": False}), 200

    except Error as e:
        print("❌ SQL ERROR:", e)
        return jsonify({"error": str(e)})
    finally:
        close_connection(conn, cursor)


# ==========================================================
# 📌 GET LIST — SORT ỔN ĐỊNH
# ==========================================================
@person_basic_bp.route("/api/person/basic", methods=["GET"])
def get_person_basic_list():
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM person WHERE birth_date IS NOT NULL;")
        print("FLASK NON NULL COUNT:", cursor.fetchone())
        cursor.execute("SELECT @@datadir;")
        print("FLASK DATADIR:", cursor.fetchone())
        cursor.execute("""
            SELECT
                person_id,
                sur_name,
                middle_name,
                last_name,
                first_name,
                gender,
                birth_date,
                death_date,
                avatar,
                avatar_path, 
                delete_status
            FROM person
            WHERE delete_status = 0
            ORDER BY
                birth_date IS NOT NULL ASC,
                birth_date ASC,
                first_name ASC;
        """)

        rows = cursor.fetchall() or []
        print("DEBUG ROWS:", rows[:2])
        for row in rows:
            row["birth_date"] = to_iso(row.get("birth_date"))
            row["death_date"] = to_iso(row.get("death_date"))

            row["avatar"] = safe_avatar_file(
                row.get("gender"),
                row.get("avatar"),
                row.get("person_id")
            )
        
        return jsonify(rows), 200

    except Error as e:
        print("❌ SQL ERROR:", e)
        return jsonify({"error": str(e)})
    finally:
        close_connection(conn, cursor)


# ==========================================================
# 📌 GET BY ID
# ==========================================================
@person_basic_bp.route("/api/person/basic/<int:id>", methods=["GET"])
def get_person_basic_by_id(id):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.person_id AS id,
                p.sur_name,
                p.middle_name,
                p.last_name,
                p.first_name,
                p.gender,
                p.birth_date,
                p.death_date,
                p.avatar,
                p.avatar_path,
                MAX(CASE WHEN pc.type = 'FATHER' THEN pc.parent_id END) AS father_id,
                MAX(CASE WHEN pc.type = 'MOTHER' THEN pc.parent_id END) AS mother_id

            FROM person p
            LEFT JOIN parent_child pc ON pc.child_id = p.person_id
            WHERE p.person_id = %s
            GROUP BY p.person_id
        """, (id,))

        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Không tìm thấy"}), 404

        row["birth_date"] = to_iso(row.get("birth_date"))
        row["death_date"] = to_iso(row.get("death_date"))

        row["avatar"] = safe_avatar_file(
            row.get("gender"),
            row.get("avatar"),
            id
        )

        return jsonify(row)

    except Error as e:
        print("❌ SQL:", e)
        return jsonify({"error": str(e)})
    finally:
        close_connection(conn, cursor)


# ==========================================================
# ➕ ADD PERSON
# ==========================================================
@person_basic_bp.route("/api/person/basic", methods=["POST"])
def add_person_basic():
    conn, cursor = None, None
    try:
        data = request.json or {}
        role = (data.get("role") or "").lower()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Duplicate check
        cursor.execute("""
            SELECT person_id FROM person
            WHERE LOWER(TRIM(REPLACE(last_name,' ','')))=LOWER(REPLACE(%s,' ','')) 
              AND LOWER(TRIM(REPLACE(first_name,' ','')))=LOWER(REPLACE(%s,' ','')) 
              AND LOWER(TRIM(gender))=LOWER(%s)
              AND delete_status=0
            LIMIT 1
        """, (
            data.get("last_name"),
            data.get("first_name"),
            data.get("gender")
        ))

        exists = cursor.fetchone()

        if exists and role in ["member_basic", "member_close"]:
            return jsonify({
                "pending": True,
                "message": "⚠️ Tồn tại — cần gửi pending."
            }), 409

        cursor.execute("""
            INSERT INTO person (
                sur_name, middle_name, last_name, first_name,
                gender, birth_date, death_date, avatar,
                delete_status, created_at, updated_at
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,0,NOW(),NOW())
        """, (
            data.get("sur_name"),
            data.get("middle_name"),
            data.get("last_name"),
            data.get("first_name"),
            data.get("gender"),
            data.get("birth_date"),
            data.get("death_date"),
            data.get("avatar"),
        ))

        conn.commit()
        return jsonify({"id": cursor.lastrowid})

    except Error as e:
        if conn:
            conn.rollback()
        print("❌ INSERT ERROR:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        close_connection(conn, cursor)


# ==========================================================
# ✏️ UPDATE
# ==========================================================
@person_basic_bp.route("/api/person/basic/<int:id>", methods=["PUT"])
def update_person_basic(id):
    conn, cursor = None, None
    try:
        data = request.json or {}

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE person
            SET sur_name=%s,
                middle_name=%s,
                last_name=%s,
                first_name=%s,
                gender=%s,
                birth_date=%s,
                death_date=%s,
                avatar=%s,
                updated_at=NOW()
            WHERE person_id=%s
        """, (
            data.get("sur_name"),
            data.get("middle_name"),
            data.get("last_name"),
            data.get("first_name"),
            data.get("gender"),
            data.get("birth_date"),
            data.get("death_date"),
            data.get("avatar"),
            id
        ))

        conn.commit()
        return jsonify({"message": "OK"})

    except Error as e:
        if conn:
            conn.rollback()
        print("❌ UPDATE ERROR:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        close_connection(conn, cursor)


# ==========================================================
# 🗑 SOFT DELETE
# ==========================================================
@person_basic_bp.route("/api/person/basic/<int:id>", methods=["DELETE"])
def delete_person_basic(id):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE person SET delete_status=1 WHERE person_id=%s",
            (id,)
        )
        conn.commit()

        return jsonify({"message": "🟡 Đã ẩn tạm"})

    except Error as e:
        if conn:
            conn.rollback()
        print("❌ DELETE ERROR:", e)
        return jsonify({"error": str(e)})
    finally:
        close_connection(conn, cursor)
