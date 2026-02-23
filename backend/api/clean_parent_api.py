from flask import Blueprint, request, jsonify
from db import get_connection

clean_parent_bp = Blueprint("clean_parent_bp", __name__)

# ================================================================
# CLEAN API: Thêm CHA / MẸ cho người đã tồn tại
# ================================================================
@clean_parent_bp.route("/api/clean/parent", methods=["POST"])
def add_parent():
    data = request.get_json() or {}

    child_id = data.get("child_id")
    parent_id = data.get("parent_id")
    relation_type = data.get("type")        # FATHER | MOTHER
    marriage_id = data.get("marriage_id")   # có thể NULL

    # -------------------------
    # Validate input cơ bản
    # -------------------------
    if not child_id or not parent_id or not relation_type:
        return jsonify({"error": "Thiếu dữ liệu bắt buộc"}), 400

    if relation_type not in ("FATHER", "MOTHER"):
        return jsonify({"error": "Loại quan hệ không hợp lệ"}), 400

    if child_id == parent_id:
        return jsonify({"error": "Cha/Mẹ và Con không thể là cùng một người"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        # -------------------------
        # Kiểm tra child tồn tại
        # -------------------------
        cur.execute(
            "SELECT person_id FROM person WHERE person_id=%s AND delete_status=0",
            (child_id,)
        )
        if not cur.fetchone():
            return jsonify({"error": "Không tìm thấy người con"}), 404

        # -------------------------
        # Kiểm tra parent tồn tại + giới tính
        # -------------------------
        cur.execute(
            "SELECT person_id, gender FROM person WHERE person_id=%s AND delete_status=0",
            (parent_id,)
        )
        parent = cur.fetchone()
        if not parent:
            return jsonify({"error": "Không tìm thấy cha/mẹ"}), 404

        if relation_type == "FATHER" and parent["gender"] != "male":
            return jsonify({"error": "Giới tính không phù hợp (FATHER phải là male)"}), 400

        if relation_type == "MOTHER" and parent["gender"] != "female":
            return jsonify({"error": "Giới tính không phù hợp (MOTHER phải là female)"}), 400

        # -------------------------
        # Kiểm tra đã có FATHER / MOTHER chưa
        # -------------------------
        cur.execute("""
            SELECT id FROM parent_child
            WHERE child_id=%s AND type=%s
        """, (child_id, relation_type))
        if cur.fetchone():
            return jsonify({"error": f"Người này đã có {relation_type}"}), 400

        # -------------------------
        # (OPTIONAL) Kiểm tra marriage nếu có
        # -------------------------
        if marriage_id:
            cur.execute(
                "SELECT id FROM marriage WHERE id=%s",
                (marriage_id,)
            )
            if not cur.fetchone():
                return jsonify({"error": "Marriage không tồn tại"}), 400
        # -------------------------
        # GUARD: Không cho trùng cha/mẹ
        # -------------------------
        cur.execute("""
            SELECT 1
            FROM parent_child
            WHERE child_id=%s AND type=%s
        """, (child_id, relation_type))

        if cur.fetchone():
            return jsonify({
                "error": f"Child already has {relation_type.lower()}"
            }), 400

        # -------------------------
        # INSERT parent_child
        # -------------------------
        cur.execute("""
            INSERT INTO parent_child (parent_id, child_id, type)
            VALUES (%s, %s, %s)
        """, (parent_id, child_id, relation_type))

        conn.commit()

        return jsonify({
            "message": "✅ Đã thêm cha/mẹ thành công",
            "child_id": child_id,
            "parent_id": parent_id,
            "type": relation_type,
            "marriage_id": marriage_id
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()
