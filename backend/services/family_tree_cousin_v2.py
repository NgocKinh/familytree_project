"""
COUSIN V2 – Ground Truth Only
---------------------------------
- Không theorem
- Không suy luận xa
- Chỉ dựa trên dữ liệu SQL ground truth
- Viết song song, KHÔNG ảnh hưởng COUSIN V1
"""


# ==============================
# Public API (V2)
# ==============================

def get_relationship_v2(db, person_a_id: int, person_b_id: int) -> dict:
    """
    Entry point COUSIN V2
    - Chỉ xử lý quan hệ ground truth
    - Không fallback sang theorem
    """

       
    # B4.1 – Parent / Child (ground truth)
    result = _gt_parent_child(db, person_a_id, person_b_id)
    if result:
        return result
    # B4.2 – Sibling (ground truth)
    result = _gt_sibling(db, person_a_id, person_b_id)
    if result:
        return result
    # B4.3 – Grandparent / Grandchild (ground truth)
    result = _gt_grandparent(db, person_a_id, person_b_id)
    if result:
        return result
    # B4.4 – Uncle / Aunt (ground truth)
    result = _gt_uncle_aunt(db, person_a_id, person_b_id)
    if result:
        return result
    # B4.5 – Nibling / Cháu (ground truth)
    result = _gt_nibling(db, person_a_id, person_b_id)
    if result:
        return result

    return {
        "relationship": "UNDETERMINED",
        "confidence": "UNKNOWN",
        "label": "Chưa xác định",
    }

# ==============================
# Ground Truth Rules (V2)
# ==============================

# B4 sẽ triển khai lần lượt:
# - parent / child
# - sibling
# - grandparent / grandchild
# - uncle / aunt (ground truth only)

def _gt_parent_child(db, person_a_id: int, person_b_id: int) -> dict | None:
    """
    Ground truth:
    - A là CHA / MẸ của B
    - A là CON của B
    """
    cursor = db.cursor(dictionary=True)

    # A là cha/mẹ của B
    cursor.execute(
        """
        SELECT type
        FROM parent_child
        WHERE parent_id = %s
          AND child_id = %s
          AND type IN ('FATHER', 'MOTHER')
        """,
        (person_a_id, person_b_id),
    )
    row = cursor.fetchone()
    if row:
        return {
            "relationship": row["type"],
            "confidence": "HIGH",
            "label": "Cha" if row["type"] == "FATHER" else "Mẹ",
        }

    # A là con của B
    cursor.execute(
        """
        SELECT type
        FROM parent_child
        WHERE parent_id = %s
          AND child_id = %s
          AND type IN ('FATHER', 'MOTHER')
        """,
        (person_b_id, person_a_id),
    )
    row = cursor.fetchone()
    if row:
        return {
            "relationship": "CHILD",
            "confidence": "HIGH",
            "label": "Con",
        }

    return None
def _gt_sibling(db, person_a_id: int, person_b_id: int) -> dict | None:
    """
    Ground truth:
    - A là ANH / EM của B nếu:
      + A ≠ B
      + Có ít nhất 1 cha hoặc mẹ ruột chung
    """
    if person_a_id == person_b_id:
        return None

    cursor = db.cursor(dictionary=True)

    # Lấy cha/mẹ ruột của A
    cursor.execute(
        """
        SELECT parent_id
        FROM parent_child
        WHERE child_id = %s
          AND type IN ('FATHER', 'MOTHER')
        """,
        (person_a_id,),
    )
    parents_a = {row["parent_id"] for row in cursor.fetchall()}
    if not parents_a:
        return None

    # Lấy cha/mẹ ruột của B
    cursor.execute(
        """
        SELECT parent_id
        FROM parent_child
        WHERE child_id = %s
          AND type IN ('FATHER', 'MOTHER')
        """,
        (person_b_id,),
    )
    parents_b = {row["parent_id"] for row in cursor.fetchall()}
    if not parents_b:
        return None

    # Có ít nhất 1 cha/mẹ chung
    if parents_a.intersection(parents_b):
        return {
            "relationship": "SIBLING",
            "confidence": "MEDIUM",
            "label": "Anh/Em",
        }

    return None
def _gt_grandparent(db, person_a_id: int, person_b_id: int) -> dict | None:
    """
    Ground truth:
    - A là ÔNG/BÀ của B nếu:
      + A là cha/mẹ của cha/mẹ của B
    - A là CHÁU của B (đảo chiều)
    """
    cursor = db.cursor(dictionary=True)

    # A là ông/bà của B
    cursor.execute(
        """
        SELECT 1
        FROM parent_child pc1
        JOIN parent_child pc2
          ON pc1.parent_id = pc2.child_id
         AND pc1.type IN ('FATHER','MOTHER')
         AND pc2.type IN ('FATHER','MOTHER')
        WHERE pc1.parent_id = %s
          AND pc1.child_id = %s
        LIMIT 1
        """,
        (person_a_id, person_b_id),
    )
    if cursor.fetchone():
        return {
            "relationship": "GRANDPARENT",
            "confidence": "MEDIUM",
            "label": "Ông/Bà",
        }

    # A là cháu của B
    cursor.execute(
        """
        SELECT 1
        FROM parent_child pc1
        JOIN parent_child pc2
          ON pc1.parent_id = pc2.child_id
         AND pc1.type IN ('FATHER','MOTHER')
         AND pc2.type IN ('FATHER','MOTHER')
        WHERE pc1.parent_id = %s
          AND pc1.child_id = %s
        LIMIT 1
        """,
        (person_b_id, person_a_id),
    )
    if cursor.fetchone():
        return {
            "relationship": "GRANDCHILD",
            "confidence": "MEDIUM",
            "label": "Cháu",
        }

    return None
def _gt_uncle_aunt(db, person_a_id: int, person_b_id: int) -> dict | None:
    """
    Ground truth:
    - A là CHÚ / BÁC / CÔ / CẬU / DÌ của B nếu:
      + A là anh/em ruột của CHA hoặc MẸ của B
    """
    cursor = db.cursor(dictionary=True)

    # 1) Lấy cha/mẹ ruột của B
    cursor.execute(
        """
        SELECT parent_id, type
        FROM parent_child
        WHERE child_id = %s
          AND type IN ('FATHER', 'MOTHER')
        """,
        (person_b_id,),
    )
    parents = cursor.fetchall()
    if not parents:
        return None

    for parent in parents:
        parent_id = parent["parent_id"]
        parent_type = parent["type"]  # FATHER / MOTHER

        # Chặn trường hợp A chính là cha/mẹ của B
        if person_a_id == parent_id:
            continue

        # 2) A có là anh/em ruột của parent không?
        sibling = _gt_sibling(db, person_a_id, parent_id)
        if not sibling or sibling.get("relationship") != "SIBLING":
            continue

        # 3) Lấy giới tính của A
        cursor.execute(
            """
            SELECT gender
            FROM person
            WHERE person_id = %s
            """,
            (person_a_id,),
        )
        row = cursor.fetchone()
        if not row:
            continue

        gender = row["gender"]

        # 4) Gán nhãn theo quy ước VN
        if parent_type == "FATHER":
            label = "Chú/Bác" if gender == "male" else "Cô"
        else:  # MOTHER
            label = "Cậu" if gender == "male" else "Dì"

        return {
            "relationship": "UNCLE_AUNT",
            "confidence": "MEDIUM",
            "label": label,
        }

    return None
def _gt_nibling(db, person_a_id: int, person_b_id: int) -> dict | None:
    """
    Ground truth:
    - A là CHÁU của B nếu:
      + B là CHÚ / BÁC / CÔ / CẬU / DÌ của A
    """
    # Đảo chiều luật B4.4, KHÔNG suy luận mới
    result = _gt_uncle_aunt(db, person_b_id, person_a_id)
    if result:
        return {
            "relationship": "NIBLING",
            "confidence": "MEDIUM",
            "label": "Cháu",
        }

    return None
