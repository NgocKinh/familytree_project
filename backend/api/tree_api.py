# ==========================================================
# File: backend/api/tree_api.py (v5.0-FINAL)
# MÔ TẢ:
#   - Auto-widowed đúng quy tắc genealogy
#   - Ưu tiên married khi có nhiều quan hệ
#   - Cohabitation không chuyển widowed, không xoá DB
#   - Không hiển thị cohabitation khi center là người married
#   - Nhưng HIỂN THỊ cohabitation khi center là người độc thân
#   - Orientation cố định theo giới tính (nam trái, nữ phải)
# ==========================================================
# ==========================================================
# SAFE FEATURE FLAG – SOCIAL CHILDREN (TẦNG 4)
# ==========================================================
ENABLE_SOCIAL_CHILDREN = False

from flask import Blueprint, jsonify
from db import get_connection
import os

tree_bp = Blueprint("tree_bp", __name__)

AVATAR_PATH = os.path.join("backend", "static", "avatars")


# ----------------------------------------------------------
# Avatar engine
# ----------------------------------------------------------
def resolve_avatar(p):
    if not p:
        return None
    pid = p["id"]
    gender = p.get("gender", "other")

    png = os.path.join(AVATAR_PATH, f"{pid}.png")
    jpg = os.path.join(AVATAR_PATH, f"{pid}.jpg")

    if os.path.exists(png):
        return f"/static/avatars/{pid}.png"
    if os.path.exists(jpg):
        return f"/static/avatars/{pid}.jpg"

    # default
    if gender == "male":
        return "/static/avatars/default_male.png"
    if gender == "female":
        return "/static/avatars/default_female.png"
    return "/static/avatars/default_other.png"


# ----------------------------------------------------------
# AUTO WIDOWED LOGIC
# ----------------------------------------------------------
def normalize_status(center, spouse, raw_status):
    """
    Quy tắc:
      - married + 1 người chết → widowed
      - separated + 1 người chết → widowed
      - divorced → giữ nguyên
      - cohabitation → giữ nguyên (KHÔNG widowed)
    """

    if not spouse:
        return None

    center_dead = center.get("death_year") is not None
    spouse_dead = spouse.get("death_year") is not None

    if raw_status in ["married", "separated"]:
        if center_dead or spouse_dead:
            return "widowed"

    # divorced & cohabitation → giữ nguyên
    return raw_status


# ----------------------------------------------------------
# LẤY NGƯỜI THEO ID
# ----------------------------------------------------------
def get_person(pid):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            person_id AS id,
            full_name_vn AS name,
            gender,
            YEAR(birth_date) AS birth_year,
            YEAR(death_date) AS death_year
        FROM person
        WHERE person_id = %s AND delete_status = 0
    """, (pid,))

    p = cur.fetchone()
    cur.close()
    conn.close()

    if p:
        p["avatar"] = resolve_avatar(p)
    return p


# ----------------------------------------------------------
# LẤY HÔN NHÂN (married / separated / divorced)
# ----------------------------------------------------------
def get_primary_marriage(pid):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            m.*,
            p.person_id AS spouse_id,
            p.full_name_vn AS name,
            p.gender,
            YEAR(p.birth_date) AS birth_year,
            YEAR(p.death_date) AS death_year
        FROM marriage m
        JOIN person p 
        ON (p.person_id = m.spouse_a_id OR p.person_id = m.spouse_b_id)
        WHERE (m.spouse_a_id = %s OR m.spouse_b_id = %s)
        AND p.person_id != %s
        ORDER BY m.start_date DESC
        LIMIT 1
    """, (pid, pid, pid))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return None

    spouse = {
        "id": row["spouse_id"],
        "name": row["name"],
        "gender": row["gender"],
        "birth_year": row["birth_year"],
        "death_year": row["death_year"],
        "avatar": resolve_avatar({
            "id": row["spouse_id"],
            "gender": row["gender"]
        })
    }

    return {
        "status": row["status"],
        "spouse": spouse
    }

# ----------------------------------------------------------
# LẤY COHABITATION (FIX: table không tồn tại thì bỏ qua)
# ----------------------------------------------------------
def get_cohabitation(pid):
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT 
                c.*,
                p.person_id AS spouse_id,
                p.full_name_vn AS name,
                p.gender,
                YEAR(p.birth_date) AS birth_year,
                YEAR(p.death_date) AS death_year
            FROM cohabitation c
            JOIN person p 
              ON (p.person_id = c.partner_a_id OR p.person_id = c.partner_b_id)
            WHERE (c.partner_a_id = %s OR c.partner_b_id = %s)
              AND p.person_id != %s
            ORDER BY c.start_date DESC
            LIMIT 1
        """, (pid, pid, pid))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return None

        spouse = {
            "id": row["spouse_id"],
            "name": row["name"],
            "gender": row["gender"],
            "birth_year": row["birth_year"],
            "death_year": row["death_year"],
            "avatar": resolve_avatar({
                "id": row["spouse_id"],
                "gender": row["gender"]
            })
        }

        return {
            "status": "cohabitation",
            "spouse": spouse
        }

    except Exception:
        # bảng cohabitation không tồn tại → coi như không có cohabitation
        return None

# ----------------------------------------------------------
# LẤY CHA MẸ
# ----------------------------------------------------------
def get_parents(pid):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            p.person_id AS id,
            p.full_name_vn AS name,
            p.gender,
            YEAR(p.birth_date) AS birth_year,
            YEAR(p.death_date) AS death_year
        FROM parent_child pc
        JOIN person p ON p.person_id = pc.parent_id
        WHERE pc.child_id = %s
    """, (pid,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    for r in rows:
        r["avatar"] = resolve_avatar(r)
    return rows


# ----------------------------------------------------------
# LẤY CON (GET BLOOD CODE)
# ----------------------------------------------------------
def get_children_by_blood(center_id, spouse_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT
            p.person_id AS id,
            p.full_name_vn AS full_name_vn,

            p.last_name   AS last_name,
            IFNULL(p.middle_name, '') AS middle_name,
            p.first_name  AS first_name,

            p.gender,
            p.blood_code,
            YEAR(p.birth_date) AS birth_year,
            YEAR(p.death_date) AS death_year
        FROM person p

        WHERE p.blood_code IS NOT NULL
          AND (
                FIND_IN_SET(%s, REPLACE(p.blood_code, '|', ','))
             OR FIND_IN_SET(%s, REPLACE(p.blood_code, '|', ','))
          )
    """, (center_id, spouse_id))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    for r in rows:
        r["avatar"] = resolve_avatar(r)

    return rows
# ==========================================================
# PARENT_CHILD.TYPE – QUY ƯỚC QUAN HỆ CHA/MẸ – CON
#
# 1. HUYẾT THỐNG (BIOLOGICAL – ĐƯỢC SUY QUAN HỆ):
#    - FATHER : cha ruột
#    - MOTHER : mẹ ruột
#
# 2. QUAN HỆ XÃ HỘI (SOCIAL – KHÔNG SUY QUAN HỆ):
#    - ADOPTED_FATHER : cha nuôi
#    - ADOPTED_MOTHER : mẹ nuôi
#    - FOSTER_FATHER  : cha đỡ đầu
#    - FOSTER_MOTHER  : mẹ đỡ đầu
#
# NGUYÊN TẮC KIẾN TRÚC:
# - family_rules.py CHỈ xử lý FATHER / MOTHER
# - Các type còn lại KHÔNG suy quan hệ huyết thống
# - Quan hệ xã hội CHỈ dùng để HIỂN THỊ trong cây gia phả
#
# TRẠNG THÁI HIỆN TẠI:
# - Code backend đã hỗ trợ đầy đủ
# - Tính năng được khóa bằng ENABLE_SOCIAL_CHILDREN
# - Chưa kích hoạt cho đến khi có dữ liệu thực tế
#
# MỤC ĐÍCH:
# - Ghi nhận quan hệ xã hội đúng đời sống
# - Không làm sai logic huyết thống
# - Cho phép mở rộng trong tương lai mà không phá hệ thống
# ==========================================================

# ----------------------------------------------------------
# LẤY CON NUÔI / CON ĐỠ ĐẦU (TẦNG 4 – QUAN HỆ XÃ HỘI)
# ----------------------------------------------------------
def get_children_social(center_id, spouse_id):
    if not ENABLE_SOCIAL_CHILDREN:
        return []

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT DISTINCT
            p.person_id AS id,
            p.full_name_vn,
            p.last_name,
            IFNULL(p.middle_name, '') AS middle_name,
            p.first_name,
            p.gender,
            p.blood_code,
            YEAR(p.birth_date) AS birth_year,
            YEAR(p.death_date) AS death_year,
            pc.type AS relation_type,
            pc.parent_id AS related_parent_id
        FROM parent_child pc
        JOIN person p ON p.person_id = pc.child_id
        WHERE pc.type IN (
            'ADOPTED_FATHER',
            'ADOPTED_MOTHER',
            'FOSTER_FATHER',
            'FOSTER_MOTHER'
        )
        AND pc.parent_id IN (%s, %s)
    """, (center_id, spouse_id))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = []

    for r in rows:
        r["avatar"] = resolve_avatar(r)
        results.append(r)

    return results


# ----------------------------------------------------------
# MAIN API
# ----------------------------------------------------------
@tree_bp.route("/family/<int:pid>", methods=["GET"])
def get_family(pid):
    # ===============================
    # 0. CENTER
    # ===============================
    center = get_person(pid)
    if not center:
        return jsonify({"error": "not_found"}), 404

    spouse = None
    status = None

    # ===============================
    # 1. HÔN NHÂN / COHAB
    # ===============================
    marriage = get_primary_marriage(pid)
    if marriage:
        spouse = marriage.get("spouse")
        status = normalize_status(center, spouse, marriage.get("status"))
    else:
        cohab = None
        if cohab:
            dead1 = center.get("death_year")
            dead2 = cohab["spouse"].get("death_year")
            if not (dead1 or dead2):
                spouse = cohab["spouse"]
                status = "cohabitation"

    # ===============================
    # 2. CHA MẸ (TẦNG 1)
    # ===============================
    father_parents = []
    mother_parents = []

    if center:
        center_parents = get_parents(center["id"]) or []

        if center.get("gender") == "male":
            father_parents = center_parents
            if spouse:
                mother_parents = get_parents(spouse["id"]) or []
        else:
            mother_parents = center_parents
            if spouse:
                father_parents = get_parents(spouse["id"]) or []

    # ===============================
    # 3. CON (TẦNG 3) – BLOOD_CODE CHUẨN
    # ===============================

    children_common = []
    children_father_separate = []
    children_mother_separate = []

    center_id = center["id"]
    spouse_id = spouse["id"] if spouse else None

    if spouse_id:
        all_children = get_children_by_blood(center_id, spouse_id)
    else:
        all_children = []

    for c in all_children:
        c["last_name"] = c.get("last_name") or ""
        c["middle_name"] = c.get("middle_name") or ""
        c["first_name"] = c.get("first_name") or ""
        try:
            father_id, mother_id = map(int, c["blood_code"].split("|"))
        except Exception:
            continue

        has_center = center_id in (father_id, mother_id)
        has_spouse = spouse_id in (father_id, mother_id)

        # ✅ con chung
        if has_center and has_spouse:
            children_common.append(c)

        # ✅ con riêng
        elif has_center and not has_spouse:
            if center["gender"] == "male":
                children_father_separate.append(c)
            else:
                children_mother_separate.append(c)

        elif has_spouse and not has_center:
            if spouse["gender"] == "male":
                children_father_separate.append(c)
            else:
                children_mother_separate.append(c)

    # ===============================
    # 3B. CON NUÔI / CON ĐỠ ĐẦU (TẦNG 4 – ẨN)
    # ===============================
    children_social = []

    if ENABLE_SOCIAL_CHILDREN and spouse_id:
        children_social = get_children_social(center_id, spouse_id)

    # ===============================
    # 4. TRẢ VỀ CHO FE
    # ===============================
    return jsonify({
        "center": center,
        "spouse": spouse,
        "marriage_status": status,

        # tầng 1
        "father_parents": father_parents,
        "mother_parents": mother_parents,

        # tầng 3 
        "children_common": children_common,
        "children_father_separate": children_father_separate,
        "children_mother_separate": children_mother_separate,

        # tầng 4 (quan hệ xã hội – mặc định rỗng)
        "children_social": children_social,
    })
