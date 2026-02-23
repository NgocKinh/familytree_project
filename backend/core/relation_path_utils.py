# print(">>> USING relation_path_utils.py (CORE) <<<")
from collections import deque


try:
    from db import get_connection
except ModuleNotFoundError:
    from backend.db import get_connection

# ================================================================
# 🔹 Lấy cha mẹ và con cái trực tiếp
# ================================================================
def get_parents_and_children(person_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    parents, children = set(), set()
    try:
        cursor.execute(
            "SELECT parent_id FROM parent_child WHERE child_id=%s;", (person_id,)
        )
        parents = {r["parent_id"] for r in cursor.fetchall()}
        cursor.execute(
            "SELECT child_id FROM parent_child WHERE parent_id=%s;", (person_id,)
        )
        children = {r["child_id"] for r in cursor.fetchall()}
    finally:
        cursor.close()
        conn.close()
    return list(parents), list(children)


def find_shortest_path_db(from_id, to_id):
    """
    PATH DISCOVERY – HÀM CHUẨN DUY NHẤT

    Mục đích:
    - Tìm đường đi ngắn nhất từ from_id → to_id
    - Chỉ làm PATH (Discovery)
    - Không suy luận quan hệ
    - Không nội / ngoại
    - Không đếm đời

    Dữ liệu sử dụng:
    - parent_child (cha ↔ con)
    - marriage (vợ ↔ chồng)

    Return:
    - [from_id, ..., to_id] nếu tìm được
    - None nếu không có đường đi
    """

    # ---------------------------------------
    # 0. Trường hợp đặc biệt
    # ---------------------------------------
    if from_id == to_id:
        return [from_id]

    # ---------------------------------------
    # 1. BUILD GRAPH (VÔ HƯỚNG)
    # ---------------------------------------

    graph: dict[int, dict[int, str]] = {}
   
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT parent_id, child_id
        FROM parent_child
    """)
    for row in cur.fetchall():
        p = row["parent_id"]
        c = row["child_id"]

        if p is None or c is None:
            continue

        graph.setdefault(p, {})[c] = "PARENT"  # p là cha/mẹ của c
        graph.setdefault(c, {})[p] = "CHILD"   # c là con của p

    # ---- Spouse ↔ Spouse
    cur.execute("""
        SELECT spouse_a_id, spouse_b_id
        FROM marriage
        WHERE status IS NULL
            OR status = 'married'
            OR status = 'separated'
            OR status = 'divorced'
            OR status = 'cohabitation'
            OR status = 'widowed'        
    """)
    for row in cur.fetchall():
        a = row["spouse_a_id"]
        b = row["spouse_b_id"]

        if a is None or b is None:
            continue

        graph.setdefault(a, {})[b] = "SPOUSE"
        graph.setdefault(b, {})[a] = "SPOUSE"


    cur.close()
    conn.close()

    # ===== SPOUSE DIRECT OVERRIDE =====
    if (
        from_id in graph
        and to_id in graph[from_id]
        and graph[from_id][to_id] == "SPOUSE"
    ):
        return [(from_id, "SPOUSE", to_id)]
    
    # ---------------------------------------
    # 2. BFS TÌM ĐƯỜNG NGẮN NHẤT (EDGE TYPE)
    # ---------------------------------------
    visited = set()
    queue = deque()

    # path = list of tuples: (from, relation, to)
    queue.append((from_id, []))
    visited.add(from_id)

    while queue:
        current, path = queue.popleft()

        for neighbor, relation in graph.get(current, {}).items():
            if neighbor in visited:
                continue

            step = (current, relation, neighbor)
            new_path = path + [step]

            if neighbor == to_id:
                return new_path

            visited.add(neighbor)
            queue.append((neighbor, new_path))


    # ---------------------------------------
    # 3. KHÔNG TÌM ĐƯỢC PATH
    # ---------------------------------------
    return None
