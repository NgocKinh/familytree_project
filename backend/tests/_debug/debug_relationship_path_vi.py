# backend/tests/_debug/debug_relationship_path_vi.py
import sys
import os

# Thêm thư mục backend vào PYTHONPATH để import db, services, src
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import sys
from db import get_connection
from src.relations.relationship_finder import find_relationship_bidirectional
from services.person_service import get_person_gender


# =====================================================
# CACHE TÊN NGƯỜI (TRÁNH QUERY LẶP)
# =====================================================
_person_name_cache = {}


def get_person_name(person_id: int) -> str:
    if person_id in _person_name_cache:
        return _person_name_cache[person_id]

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT sur_name, middle_name, first_name
        FROM person
        WHERE person_id = %s
        """,
        (person_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        name = "Unknown"
    else:
        parts = [
            row.get("sur_name"),
            row.get("middle_name"),
            row.get("first_name"),
        ]
        name = " ".join(p for p in parts if p)

    _person_name_cache[person_id] = name
    return name


# =====================================================
# XÁC ĐỊNH QUAN HỆ GIỮA 2 NODE LIỀN KỀ (TIẾNG VIỆT)
# =====================================================
def describe_edge_vi(a: int, b: int) -> str:
    conn = get_connection()
    cur = conn.cursor()

    # A là cha / mẹ của B
    cur.execute(
        """
        SELECT 1 FROM parent_child
        WHERE parent_id = %s AND child_id = %s
        """,
        (a, b),
    )
    if cur.fetchone():
        gender = get_person_gender(a)
        cur.close()
        conn.close()
        return "cha của" if gender == "male" else "mẹ của"

    # A là con của B
    cur.execute(
        """
        SELECT 1 FROM parent_child
        WHERE parent_id = %s AND child_id = %s
        """,
        (b, a),
    )
    if cur.fetchone():
        cur.close()
        conn.close()
        return "con của"

    # Hôn nhân
    cur.execute(
        """
        SELECT 1 FROM marriage
        WHERE (spouse_a_id = %s AND spouse_b_id = %s)
           OR (spouse_a_id = %s AND spouse_b_id = %s)
        """,
        (a, b, b, a),
    )
    if cur.fetchone():
        cur.close()
        conn.close()
        return "vợ/chồng của"

    # Anh / chị / em ruột (cha/mẹ chung)
    cur.execute(
        """
        SELECT 1
        FROM parent_child pc1
        JOIN parent_child pc2
          ON pc1.parent_id = pc2.parent_id
        WHERE pc1.child_id = %s
          AND pc2.child_id = %s
        """,
        (a, b),
    )
    if cur.fetchone():
        cur.close()
        conn.close()
        return "anh/chị/em ruột của"

    cur.close()
    conn.close()
    return "liên hệ với"


# =====================================================
# IN PATH TIẾNG VIỆT (ID + TÊN)
# =====================================================
def print_path_vi(path: list[int]):
    print("\n=== PATH TIẾNG VIỆT (ID + TÊN) ===")
    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]
        edge = describe_edge_vi(a, b)

        print(
            f"{a} ({get_person_name(a)}) "
            f"--{edge}--> "
            f"{b} ({get_person_name(b)})"
        )


# =====================================================
# DEBUG TỔNG HỢP
# =====================================================
def debug_relationship_path_vi(from_id: int, to_id: int):
    print("\n========================================")
    print("DEBUG RELATIONSHIP PATH (TIẾNG VIỆT)")
    print(f"A = {from_id}, B = {to_id}")
    print("========================================")

    result = find_relationship_bidirectional(from_id, to_id)

    print("\n=== ENGINE RESULT ===")
    print("A_to_B:", result.get("A_to_B"))
    print("B_to_A:", result.get("B_to_A"))

    path = result.get("path")
    if not path:
        print("\n⚠ Engine không expose path")
        return

    print("\nPATH (ID):", " -> ".join(str(x) for x in path))
    print_path_vi(path)


# =====================================================
# ENTRY POINT – NHẬN ID TỪ TERMINAL
# =====================================================
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Cách dùng:")
        print("  python tests/_debug/debug_relationship_path_vi.py <A_ID> <B_ID>")
        sys.exit(1)

    try:
        A_ID = int(sys.argv[1])
        B_ID = int(sys.argv[2])
    except ValueError:
        print("❌ A_ID và B_ID phải là số nguyên")
        sys.exit(1)

    debug_relationship_path_vi(A_ID, B_ID)

# ▶️ CÁCH SỬ DỤNG (RẤT GỌN)
# 1️⃣ Mở terminal tại thư mục backend
# cd C:\Users\RLappc.com\familytree_project\backend
# .\venv\Scripts\activate
# 2️⃣ Gõ lệnh (KHÔNG CẦN SỬA FILE)
# python tests/_debug/debug_relationship_path_vi.py 12 30
# 👉 Đổi 12 30 thành bất kỳ ID A – B nào bạn muốn test.