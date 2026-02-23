# ======================================================================
# File: backend/api/marriage.py (v4.0-UltraStable)
# Mô tả:
#   - GET ALL   /api/marriage
#   - GET ONE   /api/marriage/<id>
#   - POST      /api/marriage
#   - PUT       /api/marriage/<id>
#   - DELETE    /api/marriage/<id>
#   - Kiểm tra huyết thống nâng cao (3 đời & 5 đời)
#   - Trả về tên đầy đủ, tên hiệu, sur_name để List xử lý short/full
# ======================================================================

from flask import Blueprint, request, jsonify
from db import get_connection

marriage_bp = Blueprint("marriage_bp", __name__)

# ======================================================================
# TIỆN ÍCH CHUNG
# ======================================================================

def normalize_date(value):
    """Chuyển '' hoặc None → None (tránh lỗi MySQL)."""
    return None if value in ("", None) else value

def safe_int(value):
    """Ép kiểu an toàn."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def build_name_raw(p):
    """
    Trả về chuỗi "last|middle|first"
    Để MarriageList tự render full/short name giống PersonList.
    """
    return f"{p.get('last_name','')}|{p.get('middle_name','')}|{p.get('first_name','')}"


# ======================================================================
# KIỂM TRA HUYẾT THỐNG MỞ RỘNG
# ======================================================================

def are_blood_related(conn, id1, id2, max_depth=5):
    """BFS kiểm tra trực hệ/bàng hệ trong max_depth đời."""
    try:
        cur = conn.cursor(dictionary=True)
        visited = set()
        queue = [(id1, 0)]

        while queue:
            current_id, depth = queue.pop(0)
            if depth >= max_depth:  # quá giới hạn → bỏ
                continue

            # Lấy cha/mẹ
            cur.execute("SELECT parent_id FROM parent_child WHERE child_id=%s", (current_id,))
            parents = [r["parent_id"] for r in cur.fetchall()]

            # Lấy con
            cur.execute("SELECT child_id FROM parent_child WHERE parent_id=%s", (current_id,))
            children = [r["child_id"] for r in cur.fetchall()]

            relatives = parents + children

            for rid in relatives:
                if rid == id2:
                    return True
                if rid not in visited:
                    visited.add(rid)
                    queue.append((rid, depth + 1))

        return False

    except Exception:
        return False


# ======================================================================
# 🔹 GET ALL
# ======================================================================
@marriage_bp.route("/api/marriage", methods=["GET"])
def get_all_marriages():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
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
        """)

        rows = cur.fetchall()
        for r in rows:
            r["spouse_a_name"] = build_name_raw({
                "last_name": r["a_last"],
                "middle_name": r["a_mid"],
                "first_name": r["a_first"],
            })
            r["spouse_b_name"] = build_name_raw({
                "last_name": r["b_last"],
                "middle_name": r["b_mid"],
                "first_name": r["b_first"],
            })

        return jsonify(rows), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


# ======================================================================
# 🔹 GET ONE
# ======================================================================
@marriage_bp.route("/api/marriage/<int:mid>", methods=["GET"])
def get_marriage(mid):
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT *
            FROM marriage
            WHERE id=%s
        """, (mid,))
        row = cur.fetchone()

        if not row:
            return jsonify({"error": "Marriage not found"}), 404

        return jsonify(row), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


# ======================================================================
# 🔹 POST
# ======================================================================
@marriage_bp.route("/api/marriage", methods=["POST"])
def add_marriage():
    data = request.get_json() or {}

    spouse_a_id = safe_int(data.get("spouse_a_id"))
    spouse_b_id = safe_int(data.get("spouse_b_id"))
    start_date = normalize_date(data.get("start_date"))
    end_date = normalize_date(data.get("end_date"))
    status = data.get("status") or "married"
    ceremony_type = data.get("ceremony_type") or None
    location = data.get("location")
    notes = data.get("notes", "")
    consanguineous = int(data.get("consanguineous", 0))

    if not spouse_a_id or not spouse_b_id:
        return jsonify({"error": "Thiếu thông tin vợ/chồng!"}), 400
    if spouse_a_id == spouse_b_id:
        return jsonify({"error": "Không thể chọn cùng một người!"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        # Trùng hôn?
        cur.execute("""
            SELECT 1 FROM marriage
            WHERE (spouse_a_id=%s AND spouse_b_id=%s)
               OR (spouse_a_id=%s AND spouse_b_id=%s)
        """, (spouse_a_id, spouse_b_id, spouse_b_id, spouse_a_id))

        if cur.fetchone():
            return jsonify({"error": "Quan hệ hôn nhân này đã tồn tại!"}), 400

        # Lấy giới tính + ngày mất
        cur.execute("""
            SELECT person_id, gender, death_date
            FROM person
            WHERE person_id IN (%s,%s) AND delete_status = 0
        """, (spouse_a_id, spouse_b_id))
        people = {r["person_id"]: r for r in cur.fetchall()}

        if len(people) < 2:
            return jsonify({"error": "Một trong hai người không tồn tại!"}), 400

        g_a, g_b = people[spouse_a_id]["gender"], people[spouse_b_id]["gender"]
        d_a, d_b = people[spouse_a_id]["death_date"], people[spouse_b_id]["death_date"]

        # Không cho hôn đồng giới
        if g_a == g_b:
            return jsonify({"error": "Hai người cùng giới tính, không thể kết hôn!"}), 400

        # Ngày cưới > ngày chết ?
        if start_date:
            if d_a and start_date > str(d_a):
                return jsonify({"error": "Ngày cưới sau khi chồng đã mất!"}), 400
            if d_b and start_date > str(d_b):
                return jsonify({"error": "Ngày cưới sau khi vợ đã mất!"}), 400

        # Kiểm tra huyết thống
        related_direct = are_blood_related(conn, spouse_a_id, spouse_b_id, max_depth=5)
        related_indirect = are_blood_related(conn, spouse_a_id, spouse_b_id, max_depth=3)

        if (related_direct or related_indirect) and not consanguineous:
            return jsonify({
                "warning": "⚠️ Hai người có quan hệ huyết thống (≤5 đời). Đánh dấu 'Cùng huyết thống' để lưu."
            }), 409

        # Thêm bản ghi
        cur.execute("""
            INSERT INTO marriage
            (spouse_a_id, spouse_b_id, start_date, end_date,
             status, ceremony_type, location, notes, consanguineous)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (spouse_a_id, spouse_b_id, start_date, end_date,
              status, ceremony_type, location, notes, consanguineous))
        conn.commit()

        return jsonify({"message": "✅ Thêm quan hệ hôn nhân thành công!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


# ======================================================================
# 🔹 PUT
# ======================================================================
@marriage_bp.route("/api/marriage/<int:id>", methods=["PUT"])
def update_marriage(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM marriage WHERE id = %s", (id,))
    old = cur.fetchone()
    if not old:
        return jsonify({"error": "Marriage not found"}), 404

    data = request.json

    spouse_a_id = data.get("spouse_a_id")
    spouse_b_id = data.get("spouse_b_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    status = data.get("status")
    ceremony_type = data.get("ceremony_type")
    location = data.get("location")
    notes = data.get("notes")
    consanguineous = data.get("consanguineous", 0)

    query = """
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
    """

    cur.execute(query, (
        spouse_a_id,
        spouse_b_id,
        start_date,
        end_date,
        status,
        ceremony_type,
        location,
        notes,
        consanguineous,
        id
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "updated"})



# ======================================================================
# 🔹 DELETE
# ======================================================================
@marriage_bp.route("/api/marriage/<int:mid>", methods=["DELETE"])
def delete_marriage(mid):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM marriage WHERE id=%s", (mid,))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"error": f"Không tìm thấy ID {mid}"}), 404

        return jsonify({"message": "🗑️ Đã xóa quan hệ hôn nhân"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()
