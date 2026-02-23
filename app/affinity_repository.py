from .database import get_connection


def get_children(source_id: int):
    """
    Lấy danh sách id con trực tiếp của source
    từ bảng parent_child
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT child_id
        FROM parent_child
        WHERE parent_id = %s
    """, (source_id,))

    children = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return children

def get_current_spouses(person_id: int):
    """
    Lấy danh sách spouse id hợp lệ cho Affinity.
    Hợp lệ khi status != 'divorced'
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            CASE 
                WHEN spouse_a_id = %s THEN spouse_b_id
                ELSE spouse_a_id
            END AS spouse_id
        FROM marriage
        WHERE (spouse_a_id = %s OR spouse_b_id = %s)
          AND status != 'divorced'
    """, (person_id, person_id, person_id))

    spouses = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return spouses

def is_co_spouse(source_id: int, target_id: int):
    if source_id == target_id:
        return None

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            CASE 
                WHEN spouse_a_id = %s THEN spouse_b_id
                ELSE spouse_a_id
            END AS spouse_id
        FROM marriage
        WHERE (spouse_a_id = %s OR spouse_b_id = %s)
          AND status = 'married'
    """, (source_id, source_id, source_id))

    source_spouses = {row["spouse_id"] for row in cursor.fetchall()}

    if not source_spouses:
        cursor.close()
        conn.close()
        return None

    cursor.execute("""
        SELECT 
            CASE 
                WHEN spouse_a_id = %s THEN spouse_b_id
                ELSE spouse_a_id
            END AS spouse_id
        FROM marriage
        WHERE (spouse_a_id = %s OR spouse_b_id = %s)
          AND status = 'married'
    """, (target_id, target_id, target_id))

    target_spouses = {row["spouse_id"] for row in cursor.fetchall()}

    common = source_spouses & target_spouses

    if not common:
        cursor.close()
        conn.close()
        return None

    cursor.execute("SELECT gender FROM person WHERE person_id = %s", (source_id,))
    person = cursor.fetchone()

    cursor.close()
    conn.close()

    if not person:
        return None

    return "vợ cùng chồng" if person["gender"] == "female" else "chồng cùng vợ"

def is_parallel_sibling_in_law(source_id: int, target_id: int):
    """
    Anh/chị/em bạn rể hoặc bạn dâu
    Trường hợp: hai người kết hôn với hai anh chị em ruột
    """

    if source_id == target_id:
        return None

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 1️⃣ Lấy spouse của source và target
    cursor.execute("""
        SELECT person_id, gender
        FROM person
        WHERE person_id IN (%s, %s)
    """, (source_id, target_id))

    people = {row["person_id"]: row["gender"] for row in cursor.fetchall()}

    if len(people) != 2:
        cursor.close()
        conn.close()
        return None

    source_gender = people[source_id]
    target_gender = people[target_id]

    # Lấy spouse của source
    cursor.execute("""
        SELECT 
            CASE 
                WHEN spouse_a_id = %s THEN spouse_b_id
                ELSE spouse_a_id
            END AS spouse_id
        FROM marriage
        WHERE (spouse_a_id = %s OR spouse_b_id = %s)
          AND status = 'married'
    """, (source_id, source_id, source_id))

    source_spouses = [row["spouse_id"] for row in cursor.fetchall()]

    # Lấy spouse của target
    cursor.execute("""
        SELECT 
            CASE 
                WHEN spouse_a_id = %s THEN spouse_b_id
                ELSE spouse_a_id
            END AS spouse_id
        FROM marriage
        WHERE (spouse_a_id = %s OR spouse_b_id = %s)
          AND status = 'married'
    """, (target_id, target_id, target_id))

    target_spouses = [row["spouse_id"] for row in cursor.fetchall()]

    if not source_spouses or not target_spouses:
        cursor.close()
        conn.close()
        return None

    # 2️⃣ Kiểm tra spouse của source và target có là anh chị em ruột không
    for s_spouse in source_spouses:
        for t_spouse in target_spouses:

            cursor.execute("""
                SELECT 1
                FROM parent_child pc1
                JOIN parent_child pc2
                  ON pc1.parent_id = pc2.parent_id
                WHERE pc1.child_id = %s
                  AND pc2.child_id = %s
                LIMIT 1
            """, (s_spouse, t_spouse))

            if cursor.fetchone():
                cursor.close()
                conn.close()

                # Xác định label
                base = "bạn rể" if source_gender == "male" else "bạn dâu"
                prefix = "anh/em" if target_gender == "male" else "chị/em"

                return f"{prefix} {base}"

    cursor.close()
    conn.close()
    return None

def is_son_in_law(source_id: int, target_id: int) -> bool:
    """
    target có phải con rể của source không.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM parent_child pc
        JOIN person c ON c.person_id = pc.child_id
        JOIN marriage m ON (
            (m.spouse_a_id = c.person_id AND m.spouse_b_id = %s)
            OR
            (m.spouse_b_id = c.person_id AND m.spouse_a_id = %s)
        )
        WHERE pc.parent_id = %s
          AND c.gender = 'female'
          AND m.status != 'divorced'
        LIMIT 1
    """, (target_id, target_id, source_id))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None

def is_daughter_in_law(source_id: int, target_id: int) -> bool:
    """
    target có phải con dâu của source không.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM parent_child pc
        JOIN person c ON c.person_id = pc.child_id
        JOIN marriage m ON (
            (m.spouse_a_id = c.person_id AND m.spouse_b_id = %s)
            OR
            (m.spouse_b_id = c.person_id AND m.spouse_a_id = %s)
        )
        WHERE pc.parent_id = %s
          AND c.gender = 'male'
          AND m.status != 'divorced'
        LIMIT 1
    """, (target_id, target_id, source_id))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None

def is_brother_in_law(source_id: int, target_id: int) -> bool:
    """
    target có phải anh/em rể của source không.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM parent_child pc1
        JOIN parent_child pc2 
            ON pc1.parent_id = pc2.parent_id
        JOIN person s ON s.person_id = pc2.child_id
        JOIN marriage m ON (
            (m.spouse_a_id = s.person_id AND m.spouse_b_id = %s)
            OR
            (m.spouse_b_id = s.person_id AND m.spouse_a_id = %s)
        )
        WHERE pc1.child_id = %s
          AND pc2.child_id != %s
          AND s.gender = 'female'
          AND m.status != 'divorced'
        LIMIT 1
    """, (target_id, target_id, source_id, source_id))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None

def is_sister_in_law(source_id: int, target_id: int) -> bool:
    """
    target có phải chị/em dâu của source không.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM parent_child pc1
        JOIN parent_child pc2 
            ON pc1.parent_id = pc2.parent_id
        JOIN person s ON s.person_id = pc2.child_id
        JOIN marriage m ON (
            (m.spouse_a_id = s.person_id AND m.spouse_b_id = %s)
            OR
            (m.spouse_b_id = s.person_id AND m.spouse_a_id = %s)
        )
        WHERE pc1.child_id = %s
          AND pc2.child_id != %s
          AND s.gender = 'male'
          AND m.status != 'divorced'
        LIMIT 1
    """, (target_id, target_id, source_id, source_id))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None

def is_parent_in_law(source_id: int, target_id: int):
    """
    Trả về:
    - 'cha chồng'
    - 'mẹ chồng'
    - 'cha vợ'
    - 'mẹ vợ'
    hoặc None
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.gender AS parent_gender,
               c.gender AS spouse_gender
        FROM marriage m
        JOIN person c ON (
            (m.spouse_a_id = %s AND m.spouse_b_id = c.person_id)
            OR
            (m.spouse_b_id = %s AND m.spouse_a_id = c.person_id)
        )
        JOIN parent_child pc ON pc.child_id = c.person_id
        JOIN person p ON p.person_id = pc.parent_id
        WHERE p.person_id = %s
          AND m.status != 'divorced'
        LIMIT 1
    """, (source_id, source_id, target_id))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:
        return None

    parent_gender, spouse_gender = result

    if spouse_gender == 'male':
        return "cha chồng" if parent_gender == 'male' else "mẹ chồng"
    else:
        return "cha vợ" if parent_gender == 'male' else "mẹ vợ"

def is_sibling_in_law_reverse(source_id: int, target_id: int):
    """
    target là anh/chị/em chồng hoặc anh/chị/em vợ của source
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.gender
        FROM marriage m
        JOIN person spouse ON (
            (m.spouse_a_id = %s AND m.spouse_b_id = spouse.person_id)
            OR
            (m.spouse_b_id = %s AND m.spouse_a_id = spouse.person_id)
        )
        JOIN parent_child pc1 ON pc1.child_id = spouse.person_id
        JOIN parent_child pc2 ON pc2.parent_id = pc1.parent_id
        JOIN person s ON s.person_id = pc2.child_id
        WHERE s.person_id = %s
          AND m.status != 'divorced'
        LIMIT 1
    """, (source_id, source_id, target_id))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:
        return None

    sibling_gender = result[0]

    if sibling_gender == 'male':
        return "anh/em chồng"
    else:
        return "chị/em chồng"
