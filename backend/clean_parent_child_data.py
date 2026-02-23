import mysql.connector
from colorama import Fore, Style, init

init(autoreset=True)  # Tự reset màu log

# =========================
# 🔹 Kết nối MySQL
# =========================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Msand@167",  # ⚠️ Thay bằng mật khẩu MySQL của bạn
        database="familytreedb",
    )

# =========================
# 🔹 Dọn dữ liệu sai
# =========================
def clean_parent_child():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    print(Fore.CYAN + "🧹 Bắt đầu kiểm tra dữ liệu bảng parent_child...\n")

    # 1️⃣ Lưu backup
    print(Fore.YELLOW + "📦 Tạo bản sao dữ liệu dự phòng: parent_child_backup")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS parent_child_backup AS
        SELECT * FROM parent_child;
    """)
    conn.commit()

    # 2️⃣ Xóa quan hệ tự ngược (cha = con)
    cur.execute("SELECT id FROM parent_child WHERE parent_id = child_id;")
    same_rows = cur.fetchall()
    if same_rows:
        ids = [r["id"] for r in same_rows]
        cur.execute("DELETE FROM parent_child WHERE parent_id = child_id;")
        conn.commit()
        print(Fore.RED + f"⚠️ Đã xóa {len(ids)} bản ghi tự ngược (cha = con): {ids}")
    else:
        print(Fore.GREEN + "✅ Không có bản ghi tự ngược (cha = con).")

    # 3️⃣ Xóa quan hệ nghịch đảo trực tiếp (A→B và B→A)
    cur.execute("""
        SELECT p1.id AS id1, p2.id AS id2
        FROM parent_child p1
        JOIN parent_child p2
        ON p1.parent_id = p2.child_id AND p1.child_id = p2.parent_id
        WHERE p1.id > p2.id;
    """)
    reverse_rows = cur.fetchall()
    if reverse_rows:
        ids_to_delete = [r["id1"] for r in reverse_rows]
        cur.executemany("DELETE FROM parent_child WHERE id = %s", [(i,) for i in ids_to_delete])
        conn.commit()
        print(Fore.RED + f"⚠️ Đã xóa {len(ids_to_delete)} quan hệ nghịch đảo (cha–con ngược): {ids_to_delete}")
    else:
        print(Fore.GREEN + "✅ Không có quan hệ nghịch đảo trực tiếp.")

    # 4️⃣ Phát hiện vòng lặp gián tiếp (3 cấp)
    print(Fore.YELLOW + "\n🔍 Kiểm tra vòng lặp gián tiếp (3 cấp)...")
    cur.execute("""
        SELECT DISTINCT p1.id AS idA, p2.id AS idB, p3.id AS idC
        FROM parent_child p1
        JOIN parent_child p2 ON p1.child_id = p2.parent_id
        JOIN parent_child p3 ON p2.child_id = p3.parent_id
        WHERE p3.child_id = p1.parent_id;
    """)
    cycles = cur.fetchall()
    if cycles:
        print(Fore.RED + f"⚠️ Phát hiện {len(cycles)} vòng lặp 3 cấp:")
        for c in cycles:
            print(f"   → Liên quan ID: {c['idA']}, {c['idB']}, {c['idC']}")
        print(Fore.YELLOW + "👉 Bạn nên xem xét thủ công những ID này trước khi xóa.")
    else:
        print(Fore.GREEN + "✅ Không phát hiện vòng lặp 3 cấp.")

    # 5️⃣ Tổng kết
    print(Style.BRIGHT + Fore.CYAN + "\n🎯 Hoàn tất dọn dữ liệu bảng parent_child.")
    conn.close()


# =========================
# 🔹 Chạy script
# =========================
if __name__ == "__main__":
    try:
        clean_parent_child()
    except Exception as e:
        print(Fore.RED + f"❌ Lỗi khi dọn dữ liệu: {e}")
