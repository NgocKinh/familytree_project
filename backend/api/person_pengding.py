# ================================================================
# File: backend/api/person_pending.py (v2.0-PendingReviewClean-FINAL)
# Chức năng:
#   - Member Basic thêm TRÙNG → vào bảng person_pending (status='waiting')
#   - Member Close / Admin xem danh sách chờ
#   - Xem chi tiết pending
#   - Cập nhật pending
#   - DUYỆT → chuyển sang FormEdit với ID mới (CHƯA THÊM NGAY)
#   - HỦY DUYỆT → trả lại status='waiting'
#   - XÓA khỏi pending
# ================================================================

from flask import Blueprint, request, jsonify
from mysql.connector import Error
from db_helper import get_connection, close_connection
from datetime import datetime

person_pending_bp = Blueprint("person_pending", __name__)


# ================================================================
# 🟦 1) GET LIST — tất cả pending (status='waiting')
# ================================================================
@person_pending_bp.route("/api/person_pending", methods=["GET"])
def get_pending_list():
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                pending_id,
                sur_name,
                last_name,
                middle_name,
                first_name,
                gender,
                birth_date,
                death_date,
                reason,
                created_at,
                status,
                approved_at,
                approved_person_id
            FROM person_pending
            WHERE status = 'waiting'
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall() or []
        return jsonify(rows), 200

    except Error as e:
        print("❌ SQL ERROR @get_pending_list:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        close_connection(conn, cursor)


# ================================================================
# 🟦 2) GET DETAIL — lấy chi tiết 1 pending
# ================================================================
@person_pending_bp.route("/api/person_pending/<int:pending_id>", methods=["GET"])
def get_pending_detail(pending_id):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM person_pending
            WHERE pending_id = %s
        """, (pending_id,))

        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Không tìm thấy bản ghi"}), 404

        return jsonify(row), 200

    except Error as e:
        print("❌ SQL ERROR @get_pending_detail:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        close_connection(conn, cursor)


# ================================================================
# 🟩 3) UPDATE pending — để chỉnh sửa trước khi duyệt
# ================================================================
@person_pending_bp.route("/api/person_pending/<int:pending_id>", methods=["PUT"])
def update_pending(pending_id):
    conn, cursor = None, None
    data = request.json

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE person_pending
            SET sur_name=%s, last_name=%s, middle_name=%s, first_name=%s,
                gender=%s, birth_date=%s, death_date=%s, reason=%s,
                updated_at = NOW()
            WHERE pending_id=%s
        """

        vals = (
            data.get("sur_name"),
            data.get("last_name"),
            data.get("middle_name"),
            data.get("first_name"),
            data.get("gender"),
            data.get("birth_date"),
            data.get("death_date"),
            data.get("reason"),
            pending_id,
        )

        cursor.execute(sql, vals)
        conn.commit()

        return jsonify({"message": "✔ Đã cập nhật pending"}), 200

    except Error as e:
        print("❌ SQL ERROR @update_pending:", e)
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        close_connection(conn, cursor)


# ================================================================
# 🟩 4) APPROVE → tạo 1 record mới trong person và trả về person_id
# ================================================================
@person_pending_bp.route("/api/person_pending/approve/<int:pending_id>", methods=["PUT"])
def approve_pending(pending_id):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Lấy pending
        cursor.execute("""
            SELECT *
            FROM person_pending
            WHERE pending_id=%s AND status='waiting'
        """, (pending_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Không tồn tại hoặc đã duyệt"}), 404

        # Tạo person mới — chỉ tạo BẢN THÔ, rồi mở FormEdit để chỉnh sửa
        cursor.execute("""
            INSERT INTO person (
                sur_name, last_name, middle_name, first_name,
                gender, birth_date, death_date,
                delete_status, created_at, updated_at
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,0,NOW(),NOW())
        """, (
            row["sur_name"],
            row["last_name"],
            row["middle_name"],
            row["first_name"],
            row["gender"],
            row["birth_date"],
            row["death_date"],
        ))

        new_id = cursor.lastrowid

        # Đánh dấu pending = approved
        cursor.execute("""
            UPDATE person_pending
            SET status='approved', approved_at=NOW(), approved_person_id=%s
            WHERE pending_id=%s
        """, (new_id, pending_id))

        conn.commit()

        return jsonify({
            "message": "✔ Pending đã duyệt",
            "person_id": new_id
        }), 200

    except Error as e:
        print("❌ SQL ERROR @approve_pending:", e)
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        close_connection(conn, cursor)


# ================================================================
# 🟥 5) CANCEL APPROVAL — trả pending lại trạng thái 'waiting'
# ================================================================
@person_pending_bp.route("/api/person_pending/cancel/<int:pending_id>", methods=["PUT"])
def cancel_pending_approval(pending_id):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE person_pending
            SET status='waiting', approved_at=NULL, approved_person_id=NULL
            WHERE pending_id=%s
        """, (pending_id,))

        conn.commit()
        return jsonify({"message": "↩ Đã hủy duyệt, trả về waiting"}), 200

    except Error as e:
        print("❌ SQL ERROR @cancel_pending:", e)
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        close_connection(conn, cursor)


# ================================================================
# 🗑 6) DELETE pending — xóa hoàn toàn
# ================================================================
@person_pending_bp.route("/api/person_pending/delete/<int:pending_id>", methods=["DELETE"])
def delete_pending(pending_id):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM person_pending WHERE pending_id=%s", (pending_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Không tìm thấy bản ghi"}), 404

        return jsonify({"message": "🗑 Đã xóa pending"}), 200

    except Error as e:
        print("❌ SQL ERROR @delete_pending:", e)
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        close_connection(conn, cursor)
