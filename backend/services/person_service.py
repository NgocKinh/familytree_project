from db import get_connection

def get_person_gender(person_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT gender FROM person WHERE person_id = %s",
        (person_id,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    return row[0] if row else None
