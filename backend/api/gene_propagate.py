from db import get_connection

def safe_propagate(old_id, new_id, side, executor):
    """
    Tường lửa gene an toàn.
    Tự động sao lưu, cập nhật, và ghi log.
    side = 'father' hoặc 'mother'
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1️⃣ Sao lưu toàn bộ gene hiện tại
        cursor.execute("""
            INSERT INTO person_gene_backup (person_id, blood_code)
            SELECT id, blood_code FROM person
        """)
        conn.commit()

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

        cursor.execute(update_query)
        affected = cursor.rowcount
        conn.commit()

        # 3️⃣ Ghi log
        cursor.execute("""
            INSERT INTO gene_log (executor, old_prefix, new_prefix, affected_count)
            VALUES (%s,%s,%s,%s)
        """, (executor, str(old_id), str(new_id), affected))
        conn.commit()

        print(f"✅ Cập nhật gene hoàn tất: {affected} dòng được hiệu chỉnh an toàn ({side}).")

    except Exception as e:
        conn.rollback()
        print("⚠️ Lỗi propagate:", e)
        print("🔁 Đã rollback, dữ liệu gene an toàn.")
    finally:
        cursor.close()
        conn.close()
