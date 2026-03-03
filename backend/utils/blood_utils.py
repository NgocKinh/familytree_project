# ================================================================
# File: backend/utils/blood_utils.py
# Mục đích: Tính và cập nhật mã huyết thống (blood_code)
# ================================================================
from db import get_connection

# ------------------------------------------------
# 🔹 Hàm: cập nhật mã blood_code cho 1 người con
# ------------------------------------------------
def update_blood_code(conn, child_id):
    """
    Tính và cập nhật blood_code cho 1 người con.
    Không commit / rollback / close connection.
    """

    cur = conn.cursor(dictionary=True)

    # 🔹 Lấy cha và mẹ từ bảng parent_child
    cur.execute("""
        SELECT 
            MAX(CASE WHEN type='FATHER' THEN parent_id END) AS father_id,
            MAX(CASE WHEN type='MOTHER' THEN parent_id END) AS mother_id
        FROM parent_child
        WHERE child_id = %s;
    """, (child_id,))

    row = cur.fetchone()

    if not row:
        print(f"⚠️ Không tìm thấy cha/mẹ cho child_id={child_id}")
        cur.close()
        return

    father_id = row["father_id"] or 0
    mother_id = row["mother_id"] or 0
    blood_code = f"{father_id}|{mother_id}"

    # 🔹 Cập nhật vào bảng person
    cur.execute("""
        UPDATE person
        SET blood_code = %s
        WHERE person_id = %s;
    """, (blood_code, child_id))

    # 🔹 Sao lưu
    cur.execute("""
        INSERT INTO person_gene_backup (person_id, blood_code, backup_time)
        VALUES (%s, %s, NOW());
    """, (child_id, blood_code))

    print(f"✅ Blood_code updated for ID={child_id}: {blood_code}")

    cur.close()


# ------------------------------------------------
# 🔹 Hàm: tái tính toàn bộ blood_code
# ------------------------------------------------
def rebuild_all_blood_codes():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT DISTINCT child_id FROM parent_child;")
        all_children = [row["child_id"] for row in cur.fetchall()]

        print(f"🔄 Rebuilding {len(all_children)} blood codes...")

        for cid in all_children:
            update_blood_code(conn, cid)

        conn.commit()
        print("✅ Rebuild completed.")

    except Exception as e:
        print("❌ Error rebuilding blood codes:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()

# ------------------------------------------------
# 🔹 Test nhanh
# ------------------------------------------------
if __name__ == "__main__":
    print("🔄 Rebuild toàn bộ blood_code")
    rebuild_all_blood_codes()
