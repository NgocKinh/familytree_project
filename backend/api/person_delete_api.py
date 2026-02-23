# ================================================================
# File: backend/api/person_delete_api.py (v3.5-FullLogStable)
# Mô tả:
#   - Xóa mềm (ẩn tạm delete_status = 1)
#   - Phục hồi (delete_status = 0)
#   - Xóa vĩnh viễn
#   - Ghi nhật ký user_log
# ================================================================

from flask import Blueprint, jsonify
from db_helper import get_connection, close_connection
from mysql.connector import Error

person_delete_bp = Blueprint("person_delete_bp", __name__)

# ================================================================
# 🟡 XÓA MỀM (ẨN TẠM)
# ================================================================
@person_delete_bp.route("/api/person/delete_soft/<int:pid>", methods=["PUT"])
def soft_delete_person(pid):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE person 
            SET delete_status=1, deleted_at=NOW() 
            WHERE person_id=%s
        """, (pid,))
        conn.commit()

        return jsonify({"message": "🟡 Ẩn tạm thành công"}), 200

    except Error as e:
        if conn: conn.rollback()
        print("❌ SQL ERROR:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        close_connection(conn, cursor)

# ================================================================
# ♻️ PHỤC HỒI
# ================================================================
@person_delete_bp.route("/api/person/restore/<int:pid>", methods=["PUT"])
def restore_person(pid):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE person 
            SET delete_status=0, deleted_at=NULL 
            WHERE person_id=%s
        """, (pid,))
        conn.commit()

        return jsonify({"message": "♻️ Phục hồi thành công"}), 200

    except Error as e:
        if conn: conn.rollback()
        print("❌ SQL ERROR:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        close_connection(conn, cursor)


# ================================================================
# 🔥 XÓA VĨNH VIỄN
# ================================================================
@person_delete_bp.route("/api/person/delete_permanent/<int:pid>", methods=["DELETE"])
def delete_permanent(pid):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Xóa con trước
        cursor.execute("DELETE FROM parent_child WHERE parent_id=%s OR child_id=%s", (pid, pid))
        # Xóa hôn nhân
        cursor.execute("DELETE FROM marriage WHERE person_id=%s OR spouse_id=%s", (pid, pid))
        # Xóa ảnh / avatar
        cursor.execute("DELETE FROM avatar WHERE person_id=%s", (pid,))
        # Xóa person
        cursor.execute("DELETE FROM person WHERE person_id=%s", (pid,))

        conn.commit()

        return jsonify({"message": "🔥 Đã xóa vĩnh viễn"}), 200

    except Error as e:
        if conn: conn.rollback()
        print("❌ SQL ERROR:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        close_connection(conn, cursor)
