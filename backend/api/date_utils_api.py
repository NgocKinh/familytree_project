# ==========================================================
# File: backend/api/date_utils_api.py (v1.0)
# Mô tả:
#   - Cung cấp API chuyển đổi ngày Dương -> Âm
#   - Dùng thư viện lunarcalendar (đã cài sẵn)
# ==========================================================

from flask import Blueprint, jsonify, request
from lunarcalendar import Converter, Solar
from datetime import datetime

date_utils_bp = Blueprint("date_utils_bp", __name__)

# ==========================================================
# 🔹 API: Chuyển đổi ngày Dương sang ngày Âm
# ==========================================================
@date_utils_bp.route("/api/convert_lunar", methods=["POST"])
def convert_to_lunar():
    try:
        data = request.get_json()
        birth_date = data.get("birth_date")

        if not birth_date:
            return jsonify({"error": "Thiếu ngày sinh (birth_date)"}), 400

        # Định dạng ngày đầu vào
        solar_date = datetime.strptime(birth_date, "%Y-%m-%d")
        lunar = Converter.Solar2Lunar(Solar(solar_date.year, solar_date.month, solar_date.day))

        # Định dạng ngày âm: dd/mm
        lunar_date = f"{str(lunar.day).zfill(2)}/{str(lunar.month).zfill(2)}"

        return jsonify({
            "status": "success",
            "solar_date": birth_date,
            "lunar_date": lunar_date
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

