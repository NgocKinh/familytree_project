# ====================================================================
# File: backend/api/person_detail.py  (v2.0-FULL — chuẩn tên file)
# Mô tả:
#   - Xử lý thông tin chi tiết bảng person
#   - Đồng bộ đầy đủ tất cả cột trong bảng person
#   - Hỗ trợ email + anniversary_death
#   - Không sửa FormBasic (avatar để lại đúng chỗ)
# ====================================================================

from flask import Blueprint, jsonify, request
from db import get_connection
from datetime import datetime

person_detail_bp = Blueprint("person_detail", __name__)

# ============================================================
# 🔹 Chuẩn hoá ngày tháng (dd/mm/yyyy hoặc yyyy-mm-dd)
# ============================================================
def normalize_date(v):
    if not v:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(v, fmt).date()
        except:
            pass
    return None


# ============================================================
# 1) GET DETAIL — lấy toàn bộ thông tin chi tiết của một person
# ============================================================
@person_detail_bp.route("/api/person/detail/<int:pid>", methods=["GET"])
def get_person_detail(pid):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM person WHERE person_id = %s", (pid,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Không tìm thấy thành viên"}), 404

    return jsonify(row), 200


# ============================================================
# 2) POST DETAIL — thêm chi tiết cho person (thường không dùng)
# Chủ yếu FormBasic insert trước, Detail update ngay sau đó
# ============================================================
@person_detail_bp.route("/api/person/detail", methods=["POST"])
def add_person_detail():
    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO person (
            birth_date, birth_date_precision,
            death_date, death_date_precision,
            asian_birth_date, asian_birth_precision,
            asian_death_date, asian_death_precision,
            birth_place, death_place, grave_info, anniversary_death,
            nationality, ethnic_group, religion, languages_spoken,
            address, phone_number, email,
            school_attended, degree_earned,
            notes, updated_at
        )
        VALUES (%(birth_date)s, %(birth_date_precision)s,
                %(death_date)s, %(death_date_precision)s,
                %(asian_birth_date)s, %(asian_birth_precision)s,
                %(asian_death_date)s, %(asian_death_precision)s,
                %(birth_place)s, %(death_place)s, %(grave_info)s, %(anniversary_death)s,
                %(nationality)s, %(ethnic_group)s, %(religion)s, %(languages_spoken)s,
                %(address)s, %(phone_number)s, %(email)s,
                %(school_attended)s, %(degree_earned)s,
                %(notes)s, NOW())
    """

    cur.execute(query, {
        "birth_date": normalize_date(data.get("birth_date")),
        "birth_date_precision": data.get("birth_date_precision") or "unknown",

        "death_date": normalize_date(data.get("death_date")),
        "death_date_precision": data.get("death_date_precision") or "unknown",

        "asian_birth_date": data.get("asian_birth_date"),
        "asian_birth_precision": data.get("asian_birth_precision") or "unknown",

        "asian_death_date": data.get("asian_death_date"),
        "asian_death_precision": data.get("asian_death_precision") or "unknown",

        "birth_place": data.get("birth_place"),
        "death_place": data.get("death_place"),
        "grave_info": data.get("grave_info"),
        "anniversary_death": data.get("anniversary_death"),

        "nationality": data.get("nationality"),
        "ethnic_group": data.get("ethnic_group"),
        "religion": data.get("religion"),
        "languages_spoken": data.get("languages_spoken"),

        "address": data.get("address"),
        "phone_number": data.get("phone_number"),
        "email": data.get("email"),

        "school_attended": data.get("school_attended"),
        "degree_earned": data.get("degree_earned"),
        "notes": data.get("notes"),
    })

    conn.commit()
    new_id = cur.lastrowid

    cur.close()
    conn.close()

    return jsonify({"message": "Thêm chi tiết thành công", "person_id": new_id}), 201


# ============================================================
# 3) PUT DETAIL — cập nhật chi tiết của person
# ============================================================
@person_detail_bp.route("/api/person/detail/<int:pid>", methods=["PUT"])
def update_person_detail(pid):
    data = request.get_json()
    # -------- FIX LỖI JSON STRING -----------
    if isinstance(data, str):
        import json
        data = json.loads(data)
    # ----------------------------------------
    conn = get_connection()
    cur = conn.cursor()

    query = """
        UPDATE person SET
            birth_date=%s,
            birth_date_precision=%s,
            death_date=%s,
            death_date_precision=%s,
            asian_birth_date=%s,
            asian_birth_precision=%s,
            asian_death_date=%s,
            asian_death_precision=%s,
            birth_place=%s,
            death_place=%s,
            grave_info=%s,
            anniversary_death=%s,
            nationality=%s,
            ethnic_group=%s,
            religion=%s,
            languages_spoken=%s,
            address=%s,
            phone_number=%s,
            email=%s,
            school_attended=%s,
            degree_earned=%s,
            notes=%s,
            updated_at=NOW()
        WHERE person_id=%s
    """

    cur.execute(query, (
        normalize_date(data.get("birth_date")),
        data.get("birth_date_precision") or "unknown",

        normalize_date(data.get("death_date")),
        data.get("death_date_precision") or "unknown",

        data.get("asian_birth_date"),
        data.get("asian_birth_precision") or "unknown",

        data.get("asian_death_date"),
        data.get("asian_death_precision") or "unknown",

        data.get("birth_place"),
        data.get("death_place"),
        data.get("grave_info"),
        data.get("anniversary_death"),

        data.get("nationality"),
        data.get("ethnic_group"),
        data.get("religion"),
        data.get("languages_spoken"),

        data.get("address"),
        data.get("phone_number"),
        data.get("email"),

        data.get("school_attended"),
        data.get("degree_earned"),
        data.get("notes"),

        pid,
    ))

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Cập nhật chi tiết thành công"}), 200
