import pytest

@pytest.fixture
def family_layer1(db):
    cursor = db.cursor(dictionary=True)
    # ===== HELPER FUNCTIONS =====
    def insert_person(first_name, last_name, gender):
        cursor.execute(
            """
            INSERT INTO person (first_name, last_name, gender)
            VALUES (%s, %s, %s)
            """,
            (first_name, last_name, gender)
        )
        return cursor.lastrowid

    def insert_parent_child(parent_id, child_id, rel_type):
        cursor.execute(
            """
            INSERT INTO parent_child (parent_id, child_id, type)
            VALUES (%s, %s, %s)
            """,
            (parent_id, child_id, rel_type)
        )

    # ===== THẾ HỆ ÔNG BÀ =====
    ong_a = insert_person("Ông", "A", "male")
    ba_a  = insert_person("Bà", "A", "female")

    ong_b = insert_person("Ông", "B", "male")
    ba_b  = insert_person("Bà", "B", "female")

    # ===== THẾ HỆ CHA MẸ =====
    cha   = insert_person("Cha", "A", "male")
    me    = insert_person("Mẹ", "B", "female")
    co    = insert_person("Cô", "A", "female")

    # ===== THẾ HỆ CON =====
    con   = insert_person("Con", "A", "female")
    con2  = insert_person("Con2", "A", "male")

    stranger = insert_person("Người", "Lạ", "male")


    # ===== QUAN HỆ ÔNG BÀ → CHA / CÔ =====
    cursor.execute(
        "INSERT INTO parent_child (parent_id, child_id, type) VALUES (%s, %s, %s)",
        (ong_a, cha, "FATHER")
    )
    cursor.execute(
        "INSERT INTO parent_child (parent_id, child_id, type) VALUES (%s, %s, %s)",
        (ba_a, cha, "MOTHER")
    )

    cursor.execute(
        "INSERT INTO parent_child (parent_id, child_id, type) VALUES (%s, %s, %s)",
        (ong_a, co, "FATHER")
    )
    cursor.execute(
        "INSERT INTO parent_child (parent_id, child_id, type) VALUES (%s, %s, %s)",
        (ba_a, co, "MOTHER")
    )

    # ===== QUAN HỆ ÔNG BÀ → MẸ =====
    cursor.execute(
        "INSERT INTO parent_child (parent_id, child_id, type) VALUES (%s, %s, %s)",
        (ong_b, me, "FATHER")
    )
    cursor.execute(
        "INSERT INTO parent_child (parent_id, child_id, type) VALUES (%s, %s, %s)",
        (ba_b, me, "MOTHER")
    )

    # ===== CHA + MẸ → CON =====
    cursor.execute(
        "INSERT INTO parent_child (parent_id, child_id, type) VALUES (%s, %s, %s)",
        (cha, con, "FATHER")
    )
    cursor.execute(
        "INSERT INTO parent_child (parent_id, child_id, type) VALUES (%s, %s, %s)",
        (me, con, "MOTHER")
    )

    cursor.execute(
        "INSERT INTO parent_child (parent_id, child_id, type) VALUES (%s, %s, %s)",
        (cha, con2, "FATHER")
    )
    cursor.execute(
        "INSERT INTO parent_child (parent_id, child_id, type) VALUES (%s, %s, %s)",
        (me, con2, "MOTHER")
    )

    db.commit()

    return {
        "ong_a": ong_a,
        "ba_a": ba_a,
        "ong_b": ong_b,
        "ba_b": ba_b,
        "cha": cha,
        "me": me,
        "co": co,
        "con": con,
        "con2": con2,
        "stranger": stranger,
    }
