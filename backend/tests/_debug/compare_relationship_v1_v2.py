import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

"""
So sánh kết quả relationship giữa:
- V1: family_tree_service.get_relationship
- V2: family_tree_cousin_v2.get_relationship_v2

Mục đích:
- Debug / đối chiếu logic
- KHÔNG dùng trong production
- Chạy tay, test xong thì có thể xóa file
"""

# ==============================
# Imports
# ==============================

import backend.services.family_tree_service as v1
import backend.services.family_tree_cousin_v2 as v2

# Import hàm lấy DB theo đúng project của bạn
# Nếu project bạn dùng cách khác, chỉ cần sửa dòng này
from backend.db import get_connection


# ==============================
# Compare helper
# ==============================

def compare(db, person_a_id: int, person_b_id: int):
    """
    So sánh kết quả V1 vs V2 cho 1 cặp người
    """
    # BẬT V2 (rất quan trọng: bật trên MODULE, không phải biến local)
    v2.COUSIN_V2_ENABLED = True

    r1 = v1.get_relationship(db, person_a_id, person_b_id)
    r2 = v2.get_relationship_v2(db, person_a_id, person_b_id)

    print("=" * 60)
    print(f"A = {person_a_id}, B = {person_b_id}")
    print("V1:", r1)
    print("V2:", r2)
    print("=" * 60)
    print()


# ==============================
# Main (chạy tay)
# ==============================

if __name__ == "__main__":
    db = get_connection()

    # ==========================
    # DANH SÁCH CASE TEST
    # (thay bằng ID thật trong DB của bạn)
    # ==========================

    test_cases = [
        (5, 11),   # ví dụ: cha -> con
        (11, 5),   # con -> cha
        (4, 5),   # anh/em
        (7, 11),   # ông/bà -> cháu
        (12, 7),   # cháu -> ông/bà
        (4, 11),   # chú/bác/cô/cậu/dì -> cháu
        (11, 4),   # cháu -> chú/bác/cô/cậu/dì
        (11, 42),  # cousin (V1 có, V2 thường không)
        (13, 7), # không quan hệ
    ]

    for a, b in test_cases:
        compare(db, a, b)

