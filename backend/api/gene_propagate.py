from db import get_connection

def safe_propagate(conn, old_id, new_id, side, executor):
    """
    Tường lửa gene an toàn.
    side = 'FATHER' hoặc 'MOTHER'
    """

    cur = conn.cursor(dictionary=True)

    # 1️⃣ Sao lưu toàn bộ gene hiện tại
    cur.execute("""
        INSERT INTO person_gene_backup (person_id, blood_code)
        SELECT person_id, blood_code FROM person
    """)

    # 2️⃣ Cập nhật theo phía cha hoặc mẹ
    if side == "FATHER":
        update_query = f"""
            UPDATE person
            SET blood_code = CONCAT({new_id}, SUBSTRING(blood_code, INSTR(blood_code, '-')))
            WHERE blood_code LIKE '{old_id if old_id else "%"}-%';
        """
    else:
        update_query = f"""
            UPDATE person
            SET blood_code = CONCAT(SUBSTRING_INDEX(blood_code, '-', 1), '-{new_id}')
            WHERE blood_code LIKE '%-{old_id if old_id else "%"}';
        """

    cur.execute(update_query)
    affected = cur.rowcount

    # 3️⃣ Ghi log
    cur.execute("""
        INSERT INTO gene_log (executor, old_prefix, new_prefix, affected_count)
        VALUES (%s,%s,%s,%s)
    """, (executor, str(old_id), str(new_id), affected))

    print(f"✅ Gene propagate OK: {affected} rows updated ({side}).")

    cur.close()
