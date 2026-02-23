import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Msand@167",
    "database": "familytreedb"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_family_path(source_id: int, target_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.callproc('get_family_path', [source_id, target_id])

    result = None
    for res in cursor.stored_results():
        row = res.fetchone()
        if row:
            result = row

    cursor.close()
    conn.close()

    if not result:
        return None

    direction_path = result[0]
    gender_path = result[1]
    lineage_path = result[2]
    depth = result[3]

    return {
        "direction_path": direction_path,
        "gender_path": gender_path,
        "lineage_path": lineage_path,
        "depth": depth
    }

def get_spouse_relationship(source_id: int, target_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.gender
        FROM marriage m
        JOIN person p ON (
            (m.spouse_a_id = %s AND m.spouse_b_id = p.person_id)
            OR
            (m.spouse_b_id = %s AND m.spouse_a_id = p.person_id)
        )
        WHERE p.person_id = %s
        LIMIT 1
    """, (source_id, source_id, target_id))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:
        return None

    if result["gender"] == "male":
        return "chồng"
    else:
        return "vợ"
