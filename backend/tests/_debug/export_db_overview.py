# backend/tests/_debug/export_db_overview.py
import sys
import os

# Thêm thư mục backend vào PYTHONPATH
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from db import get_connection

OUTPUT_FILE = "person_ids.txt"


def export_db_overview():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        # ==================================================
        # 1. PERSON LIST
        # ==================================================
        f.write("===== PERSON LIST =====\n")
        cur.execute("""
            SELECT
                person_id,
                gender,
                CONCAT_WS(' ', sur_name, last_name, middle_name, first_name) AS full_name
            FROM person
            ORDER BY person_id
        """)
        persons = cur.fetchall()
        for p in persons:
            f.write(
                f"{p['person_id']:>5} | {p['gender'] or '-':>6} | {p['full_name']}\n"
            )

        f.write("\n")

        # ==================================================
        # 2. MARRIAGE LIST
        # ==================================================
        f.write("===== MARRIAGE LIST =====\n")
        cur.execute("""
            SELECT
                m.id AS marriage_id,
                m.spouse_a_id,
                pa.gender AS gender_a,
                CONCAT_WS(' ', pa.sur_name, pa.last_name, pa.middle_name, pa.first_name) AS name_a,
                m.spouse_b_id,
                pb.gender AS gender_b,
                CONCAT_WS(' ', pb.sur_name, pb.last_name, pb.middle_name, pb.first_name) AS name_b,
                m.status
            FROM marriage m
            JOIN person pa ON pa.person_id = m.spouse_a_id
            JOIN person pb ON pb.person_id = m.spouse_b_id
            ORDER BY m.id
        """)
        marriages = cur.fetchall()
        for m in marriages:
            f.write(
                f"{m['marriage_id']:>5} | "
                f"{m['spouse_a_id']} ({m['gender_a']}) {m['name_a']}  <->  "
                f"{m['spouse_b_id']} ({m['gender_b']}) {m['name_b']}  "
                f"[{m['status']}]\n"
            )

        f.write("\n")

        # ==================================================
        # 3. PARENT_CHILD LIST
        # ==================================================
        f.write("===== PARENT - CHILD LIST =====\n")
        cur.execute("""
            SELECT
                pc.parent_id,
                pp.gender AS parent_gender,
                CONCAT_WS(' ', pp.sur_name, pp.last_name, pp.middle_name, pp.first_name) AS parent_name,
                pc.child_id,
                cp.gender AS child_gender,
                CONCAT_WS(' ', cp.sur_name, cp.last_name, cp.middle_name, cp.first_name) AS child_name
            FROM parent_child pc
            JOIN person pp ON pp.person_id = pc.parent_id
            JOIN person cp ON cp.person_id = pc.child_id
            ORDER BY pc.parent_id, pc.child_id
        """)
        relations = cur.fetchall()
        for r in relations:
            f.write(
                f"{r['parent_id']} ({r['parent_gender']}) {r['parent_name']}  ->  "
                f"{r['child_id']} ({r['child_gender']}) {r['child_name']}\n"
            )

    cur.close()
    conn.close()

    print(f"✔ Đã xuất DB overview vào file: {OUTPUT_FILE}")
    print(f"  - Persons   : {len(persons)}")
    print(f"  - Marriages : {len(marriages)}")
    print(f"  - Relations : {len(relations)}")


if __name__ == "__main__":
    export_db_overview()

# ▶️ CÁCH SỬ DỤNG (RẤT GỌN)
# 1️⃣ Mở terminal tại thư mục backend
# cd C:\Users\RLappc.com\familytree_project\backend 
# venv\Scripts\activate
# python tests/_debug/export_db_overview.py
# 👉 Sau khi chạy xong, bạn sẽ có file:
# backend/person_ids.txt