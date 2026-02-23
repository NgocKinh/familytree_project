def create_child_from_marriage(db, marriage_id: int, child_data: dict) -> int:
    cursor = db.cursor(dictionary=True)

    try:
        # 1. Lấy marriage
        cursor.execute(
            "SELECT spouse_a_id, spouse_b_id FROM marriage WHERE id = %s",
            (marriage_id,),
        )
        marriage = cursor.fetchone()
        if not marriage:
            raise Exception("Marriage not found")

        spouse_a_id = marriage["spouse_a_id"]
        spouse_b_id = marriage["spouse_b_id"]

        # 2. Lấy gender
        cursor.execute(
            """
            SELECT person_id, gender
            FROM person
            WHERE person_id IN (%s, %s)
            """,
            (spouse_a_id, spouse_b_id),
        )
        spouses = cursor.fetchall()

        genders = {s["gender"] for s in spouses}
        if genders != {"male", "female"}:
            raise Exception("Marriage must have 1 male and 1 female")
        father_id = None
        mother_id = None

        for s in spouses:
            if s["gender"] == "male":
                father_id = s["person_id"]
            elif s["gender"] == "female":
                mother_id = s["person_id"]

        if not father_id or not mother_id:
            raise Exception("Marriage must have exactly 1 father and 1 mother")

        # 3. Insert child
        cursor.execute(
            "INSERT INTO person (last_name, first_name, gender) VALUES (%s, %s, %s)",
            (
                child_data.get("last_name", "Trần"),
                child_data["first_name"],
                child_data.get("gender", "other"),
            ),
        )
        child_id = cursor.lastrowid

        # 4. Insert parent_child
        cursor.execute(
            "INSERT INTO parent_child (parent_id, child_id, marriage_id, type) VALUES (%s, %s, %s, %s)",
            (father_id, child_id, marriage_id, "FATHER"),
        )

        cursor.execute(
            "INSERT INTO parent_child (parent_id, child_id, marriage_id, type) VALUES (%s, %s, %s, %s)",
            (mother_id, child_id, marriage_id, "MOTHER"),
        )

        db.commit()
        return child_id

    except Exception:
        db.rollback()
        raise


def get_relationship(
    db,
    person_a_id: int,
    person_b_id: int,
    enable_theorem: bool = True
) -> dict:

    # ===============================
    # TẦNG 2 – THEOREM (suy luận xa)
    # ===============================
    if enable_theorem:
        theorem_result = get_relationship_theorem(
            db=db,
            person_a_id=person_a_id,
            person_b_id=person_b_id
        )
        if theorem_result:
            return theorem_result


    return {
        "relationship": "UNDETERMINED",
        "confidence": "UNKNOWN",
        "label": "Chưa xác định",
    }

def get_relationship_theorem(
    db,
    person_a_id: int,
    person_b_id: int,
    depth: int = 0,
    max_depth: int = 3
) -> dict | None:

    """
    TẦNG 2 – Suy luận quan hệ xa (<= 4 đời)
    - KHÔNG tạo luật mới
    - CHỈ kết hợp kết quả từ get_relationship (Tầng 1)
    """
    if depth >= max_depth:
        return None
    # THEOREM T2-COUSIN:
    # A và B là COUSIN nếu:
    # - Cha/mẹ của A và cha/mẹ của B là anh/chị/em ruột
    # - Suy luận từ bảng parent_child, không tạo luật mới
    # Lấy danh sách cha/mẹ của A bằng cách duyệt person

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT parent_id
        FROM parent_child
        WHERE child_id = %s
    """, (person_a_id,))
    parents = [row["parent_id"] for row in cursor.fetchall()]

    if not parents:
        return None

    # Với mỗi cha/mẹ của A, tìm anh/chị/em của họ
    for parent_id in parents:
        cursor.execute("""
            SELECT child_id
            FROM parent_child
            WHERE parent_id IN (
                SELECT parent_id
                FROM parent_child
                WHERE child_id = %s
            )
            AND child_id != %s
        """, (parent_id, parent_id))
        siblings = [row["child_id"] for row in cursor.fetchall()]

        for sibling_id in siblings:
            # Kiểm tra sibling đó có là cha/mẹ của B không
            cursor.execute("""
                SELECT 1
                FROM parent_child
                WHERE parent_id = %s
                    AND child_id = %s
                    AND type IN ('FATHER','MOTHER')
            """, (sibling_id, person_b_id))

            if cursor.fetchone():
                return {
                    "relationship": "COUSIN",
                    "confidence": "HIGH",
                    "label": "Anh em họ"
                }
    # THEOREM T2 – CÔ / CHÚ / BÁC / CẬU / DÌ HỌ
    result = get_uncle_aunt_cousin_relationship(db, person_a_id, person_b_id)
    if result:
        return result

    # THEOREM T2 – CHÁU HỌ
    result = get_uncle_aunt_cousin_reverse_relationship(db, person_a_id, person_b_id)
    if result:
        return result
    # THEOREM T2 – COUSIN BẬC 2
    # Cha/mẹ của A là COUSIN của cha/mẹ của B
    for parent_a in parents:
        cursor.execute("""
            SELECT parent_id
            FROM parent_child
            WHERE child_id = %s
        """, (person_b_id,))
        parents_b = [row["parent_id"] for row in cursor.fetchall()]

        for parent_b in parents_b:
            cousin_check = get_relationship_theorem(
                db=db,
                person_a_id=parent_a,
                person_b_id=parent_b,
                depth=depth + 1,
                max_depth=max_depth
            )

            if cousin_check and cousin_check.get("relationship") == "COUSIN":
                return attach_generation_offset(
                    {
                        "relationship": "COUSIN",
                        "confidence": "LOW",
                        "label": "Anh em họ (bậc 2)",
                    },
                    offset=0,
                    degree=2
                )

    return None

def get_grandparent_relationship(db, grandparent_id: int, grandchild_id: int) -> dict:
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT child_id
        FROM parent_child
        WHERE parent_id = %s
        """,
        (grandparent_id,),
    )
    parents = cursor.fetchall()
    if not parents:
        return None

    parent_ids = [p["child_id"] for p in parents]

    # === ĐOẠN ĐÃ SỬA ===
    placeholders = ",".join(["%s"] * len(parent_ids))
    sql = f"""
        SELECT type
        FROM parent_child
        WHERE parent_id IN ({placeholders})
          AND child_id = %s
          AND type IN ('FATHER', 'MOTHER')
    """
    cursor.execute(sql, (*parent_ids, grandchild_id))
    row = cursor.fetchone()

    if row:
        return {
            "relationship": "GRANDPARENT",
            "confidence": "MEDIUM",
            "label": "Ông/Bà",
        }

    return None

def get_sibling_relationship(db, person_a_id: int, person_b_id: int) -> dict:
    """
    Luật 1.3A – Anh/Em (luật gốc)
    A là anh/em của B nếu:
    - A ≠ B
    - A và B có ít nhất một cha hoặc mẹ ruột chung
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

    # Giao nhau = có cha/mẹ chung
    if parents_a.intersection(parents_b):
        return {
            "relationship": "SIBLING",
            "confidence": "MEDIUM",
            "label": "Anh/Em",
        }

    return None

def get_uncle_aunt_cousin_relationship(db, person_a_id: int, person_b_id: int) -> dict | None:
    """
    A là cô/chú/bác/cậu/dì HỌ của B nếu:
    A và cha/mẹ của B là COUSIN
    """

    cursor = db.cursor(dictionary=True)

    # Lấy cha/mẹ của A
    cursor.execute("""
        SELECT parent_id
        FROM parent_child
        WHERE child_id = %s
          AND type IN ('FATHER', 'MOTHER')
    """, (person_a_id,))
    parents_a = [row["parent_id"] for row in cursor.fetchall()]

    if not parents_a:
        return None

    # Lấy cha/mẹ của B
    cursor.execute("""
        SELECT parent_id, type
        FROM parent_child
        WHERE child_id = %s
          AND type IN ('FATHER', 'MOTHER')
    """, (person_b_id,))
    parents_b = cursor.fetchall()

    if not parents_b:
        return None

    for pb in parents_b:
        parent_b_id = pb["parent_id"]
        parent_type = pb["type"]

        # Lấy cha/mẹ của parent B
        cursor.execute("""
            SELECT parent_id
            FROM parent_child
            WHERE child_id = %s
              AND type IN ('FATHER', 'MOTHER')
        """, (parent_b_id,))
        grandparents_b = {row["parent_id"] for row in cursor.fetchall()}

        # Kiểm tra cha/mẹ của A có chung ông bà với parent B không
        for pa in parents_a:
            cursor.execute("""
                SELECT parent_id
                FROM parent_child
                WHERE child_id = %s
                  AND type IN ('FATHER', 'MOTHER')
            """, (pa,))
            grandparents_a = {row["parent_id"] for row in cursor.fetchall()}

            if grandparents_a.intersection(grandparents_b):
                cursor.execute("""
                    SELECT gender
                    FROM person
                    WHERE person_id = %s
                """, (person_a_id,))
                row = cursor.fetchone()
                if not row:
                    return None

                gender = row["gender"]

                if parent_type == "FATHER":
                    label = "Chú/Bác họ" if gender == "male" else "Cô họ"
                else:
                    label = "Cậu họ" if gender == "male" else "Dì họ"

                return {
                    "relationship": "UNCLE_AUNT_COUSIN",
                    "confidence": "HIGH",
                    "label": label
                }

    return None

def get_uncle_aunt_reverse_relationship(db, person_a_id: int, person_b_id: int) -> dict:
    """
    LUẬT 1.4B – CHÁU (đảo của CHÚ / BÁC / CÔ / CẬU / DÌ)

    A là CHÁU của B nếu:
    - B là chú/bác/cô/cậu/dì của A (theo luật 1.4)
    """

    # Tái sử dụng LUẬT 1.4, KHÔNG suy luận mới
    reverse_check = get_uncle_aunt_cousin_relationship(
        db=db,
        person_a_id=person_b_id,  # ĐẢO CHIỀU
        person_b_id=person_a_id
    )

    if reverse_check:
        return {
            "relationship": "NIBLING",  # cháu gọi chú/bác/cô/cậu/dì
            "confidence": "MEDIUM",
            "label": "Cháu",
        }

    return None

def get_uncle_aunt_cousin_relationship(db, person_a_id: int, person_b_id: int) -> dict | None:
    """
    TẦNG 2 – CÔ / CHÚ / BÁC / CẬU / DÌ HỌ

    A là cô/chú/bác/cậu/dì HỌ của B nếu:
    - A là COUSIN của cha hoặc mẹ của B
    """

    cursor = db.cursor(dictionary=True)
    # FIX DỨT ĐIỂM: kiểm tra cô/chú họ bằng SQL đã verify
    cursor.execute("""
          SELECT 1
          FROM parent_child pc_b
          JOIN parent_child pc_p
            ON pc_b.parent_id = pc_p.child_id
           AND pc_b.type IN ('FATHER','MOTHER')
           AND pc_p.type IN ('FATHER','MOTHER')
          JOIN parent_child pc_sib
            ON pc_p.parent_id = pc_sib.parent_id
           AND pc_sib.type IN ('FATHER','MOTHER')
          JOIN parent_child pc_a_parent
            ON pc_sib.child_id = pc_a_parent.parent_id
           AND pc_a_parent.type IN ('FATHER','MOTHER')
          WHERE pc_b.child_id = %s
            AND pc_a_parent.child_id = %s
          LIMIT 1
    """, (person_b_id, person_a_id))


    if cursor.fetchone():
        cursor.execute("""
            SELECT gender
            FROM person
            WHERE person_id = %s
        """, (person_a_id,))
        row = cursor.fetchone()

        label = "Cô họ" if row and row["gender"] == "female" else "Chú họ"

        return attach_generation_offset(
            {
                "relationship": "UNCLE_AUNT_COUSIN",
                "confidence": "LOW",
                "label": label,
            },
            offset=-1
        )

    cursor.execute("""
        SELECT parent_id, type
        FROM parent_child
        WHERE child_id = %s
          AND type IN ('FATHER', 'MOTHER')
    """, (person_b_id,))
    parents = cursor.fetchall()
    if not parents:
        return None

    for parent in parents:
        parent_id = parent["parent_id"]
        parent_type = parent["type"]

        # FIX: kiểm tra COUSIN của cha/mẹ bằng SQL đã verify
        cursor.execute("""
            SELECT 1
            FROM parent_child pc_b
            JOIN parent_child pc_p        ON pc_b.parent_id = pc_p.child_id
            JOIN parent_child pc_sib      ON pc_p.parent_id = pc_sib.parent_id
            JOIN parent_child pc_a_parent ON pc_sib.child_id = pc_a_parent.parent_id
            WHERE pc_b.child_id = %s
                AND pc_a_parent.child_id = %s
                LIMIT 1
            """, (person_b_id, person_a_id))

        if not cursor.fetchone():
            continue

        cursor.execute("""
            SELECT gender
            FROM person
            WHERE person_id = %s
        """, (person_a_id,))
        row = cursor.fetchone()
        if not row:
            continue

        gender = row["gender"]

        if parent_type == "FATHER":
            label = "Chú/Bác họ" if gender == "male" else "Cô họ"
            offset = -1
        else:
            label = "Cậu họ" if gender == "male" else "Dì họ"
            offset = -1

        return attach_generation_offset(
            {
                "relationship": "UNCLE_AUNT_COUSIN",
                "confidence": "LOW",
                "label": label,
            },
            offset=offset
        )

    return None

def get_uncle_aunt_cousin_reverse_relationship(db, person_a_id: int, person_b_id: int) -> dict | None:
    """
    TẦNG 2 – CHÁU HỌ
    (đảo của CÔ / CHÚ / BÁC / CẬU / DÌ HỌ)
    """

    reverse_check = get_uncle_aunt_cousin_relationship(
        db=db,
        person_a_id=person_b_id,
        person_b_id=person_a_id
    )

    if reverse_check:
        return attach_generation_offset(
            {
                "relationship": "NIBLING_COUSIN",
                "confidence": "LOW",
                "label": "Cháu họ",
            },
            offset=+1
        )

    return None

def attach_generation_offset(result: dict, offset: int, degree: int | None = None) -> dict:
    """
    Gắn thông tin thế hệ cho quan hệ suy luận (Tầng 2+)
    """
    result["generation_offset"] = offset
    if degree is not None:
        result["degree"] = degree
    return result
