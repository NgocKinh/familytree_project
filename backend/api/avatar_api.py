from flask import Blueprint, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from db import get_connection
from PIL import Image  # ✅ dùng để convert PNG → JPG

avatar_bp = Blueprint("avatar_bp", __name__)

# ==========================================================
# 🔹 Đường dẫn tuyệt đối chính xác tới thư mục chứa ảnh
# ==========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "avatars")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ==========================================================
# 🔹 API upload ảnh đại diện
# ==========================================================
@avatar_bp.route("/api/avatar/upload/<int:person_id>", methods=["POST"])
def upload_avatar(person_id):
    if "file" not in request.files:
        return jsonify({"error": "Không có file upload"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Chưa chọn file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit(".", 1)[1].lower()
        new_filename = f"{person_id}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, new_filename)

        # 🔸 Xóa ảnh cũ (nếu tồn tại)
        for old_ext in ["jpg", "jpeg", "png"]:
            old_path = os.path.join(UPLOAD_FOLDER, f"{person_id}.{old_ext}")
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except Exception as e:
                    print(f"Lỗi xóa ảnh cũ: {e}")

        # 🔸 Nếu file là PNG → convert sang JPG bằng Pillow
        if ext == "png":
            try:
                image = Image.open(file.stream).convert("RGB")
                image.save(filepath, "JPEG", quality=90)
            except Exception as e:
                return jsonify({"error": f"Lỗi chuyển PNG sang JPG: {e}"}), 500
        else:
            # 🔸 Nếu là JPG thì lưu thẳng
            file.save(filepath)

        # 🔸 Cập nhật DB
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE person SET avatar = %s WHERE person_id = %s",
            (f"avatars/{new_filename}", person_id),
        )
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "message": "Upload thành công",
            "filename": new_filename
        }), 200

    return jsonify({"error": "File không hợp lệ (chỉ chấp nhận .jpg hoặc .png)"}), 400


# ==========================================================
# 🔹 API trả ảnh tĩnh (mặc định và upload)
# ==========================================================
@avatar_bp.route("/avatars/<path:filename>")
def get_avatar(filename):
    # ✅ đảm bảo Flask luôn tìm đúng thư mục tuyệt đối
    return send_from_directory(UPLOAD_FOLDER, filename)

