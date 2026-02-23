# ================================================================
# File: backend/api/relation_api.py (v2.1-safe)
# Mô tả:
#   - Giữ nguyên kiến trúc ổn định của v2.0
#   - Thêm cơ chế kiểm tra an toàn tránh lỗi NoneType
#   - Khi find_relation() lỗi hoặc trả None, vẫn phản hồi hợp lệ
# ================================================================

from flask import Blueprint, request, jsonify
from api.relation_utils import find_relation  # Hàm xử lý chính

from api.auth import require_auth, require_role

# ================================================================
# 🔹 Blueprint khởi tạo
# ================================================================
relation_bp = Blueprint("relation_bp", __name__)

# ================================================================
# 🔹 API: Xác định mối quan hệ giữa hai người
# ================================================================
@relation_bp.route("/relation/find", methods=["POST"])
@require_auth
@require_role("member_basic", "member_close", "co_operator", "admin")
def relation_find():
    """
    API nhận vào 2 ID người (person_a_id, person_b_id),
    gọi thuật toán find_relation() và trả về mô tả mối quan hệ chi tiết.
    Giữ nguyên cấu trúc phản hồi cũ để không phá vỡ frontend.
    """
    try:
        # ------------------------------------------------------------
        # Lấy dữ liệu JSON gửi từ frontend
        # ------------------------------------------------------------
        data = request.get_json(silent=True) or {}
        person_a = data.get("person_a_id")
        person_b = data.get("person_b_id")

        # ------------------------------------------------------------
        # Kiểm tra dữ liệu đầu vào
        # ------------------------------------------------------------
        if not person_a or not person_b:
            return jsonify({"error": "Thiếu ID hai người"}), 400

        # ------------------------------------------------------------
        # Gọi hàm xử lý chính trong relation_utils (đã nâng cấp v2.0)
        # ------------------------------------------------------------
        # result = find_relation(person_a, person_b) or {}

      

        # ------------------------------------------------------------
        # Đảm bảo kết quả luôn là dict an toàn
        # ------------------------------------------------------------
        if not isinstance(result, dict):
            result = {
                "relation_basic": "Không xác định",
                "relation_detail": "Không có dữ liệu",
                "relation_path": []
            }

        # ------------------------------------------------------------
        # Trả kết quả dạng JSON (giữ format cũ để frontend hoạt động)
        # ------------------------------------------------------------
        print("DEBUG API RESPONSE:", result)
        return jsonify({
            "person_a": person_a,
            "person_b": person_b,
            "relation": result.get("relation_detail", result.get("relation", "")),
            "relation_basic": result.get("relation_basic", ""),
            "relation_detail": result.get("relation_detail", ""),
            "relation_path": result.get("relation_path", [])
        }), 200

    except Exception as e:
        print("❌ Lỗi trong relation_find:", e)
        
        return jsonify({"error": str(e)}), 500
