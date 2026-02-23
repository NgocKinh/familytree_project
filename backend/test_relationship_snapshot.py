# SNAPSHOT – FINAL E2E (sau khi 5 tầng đã PASS)
from core.relation_path_utils import find_relationship_bidirectional
SNAPSHOT = {
    (5, 11): ('Cha', 'Con'),
    (11, 5): ('Con', 'Cha'),
    (5, 8):  ('Chồng', 'Vợ'),
}

for (a, b), (ab, ba) in SNAPSHOT.items():
    r = find_relationship_bidirectional(a, b)
    assert r['A_to_B'] == ab and r['B_to_A'] == ba

# CÁCH CHẠY ĐÚNG FILE TEST (THEO HỆ CỦA BẠN)
# Bước 1 – Mở terminal
# Bước 2 – Đứng trong thư mục backend
    # cd familytree_project/backend
# Bước 3 – Chạy test
    # python test_relationship_snapshot.py

# KHI NÀO COI LÀ PASS / FAIL?
    # ✅ PASS
    # Không in gì
    # Không error
    # Terminal quay về prompt
# 👉 OK – thay đổi được chấp nhận

    # ❌ FAIL
    # Có AssertionError
    # Hoặc trace bất kỳ
# 👉 Không merge – không giữ – quay lại sửa hoặc bỏ