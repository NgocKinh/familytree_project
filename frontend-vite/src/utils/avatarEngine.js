// ======================================================================
// File: src/utils/avatarEngine.js
// Mô tả:
//   - Quy chuẩn avatar duy nhất cho toàn hệ thống
//   - Ưu tiên ảnh thật theo ID (.jpg → .png)
//   - Nếu fail → avatar mặc định theo giới tính
// ======================================================================

import maleAvatar from "../assets/male.png";
import femaleAvatar from "../assets/female.png";
import otherAvatar from "../assets/other.png";

const BASE = "http://127.0.0.1:8010/api/static/avatars/";

// ======================================================
// Lấy URL avatar theo ID
// ======================================================
export function getAvatarURL(id, gender) {
  if (!id) return fallbackAvatar(gender);

  // thử JPG trước
  return `${BASE}${id}.jpg?t=${Date.now()}`;
}

// ======================================================
// Hàm fallback theo giới tính
// ======================================================
export function fallbackAvatar(gender) {
  if (gender === "male") return maleAvatar;
  if (gender === "female") return femaleAvatar;
  return otherAvatar;
}

// ======================================================
// Xử lý khi ảnh lỗi → chuyển sang PNG → rồi fallback
// ======================================================
export function handleAvatarError(e, id, gender) {
  const src = e.target.src;

  // Nếu đang load .jpg → thử .png
  if (src.includes(".jpg")) {
    e.target.onerror = null; // tránh vòng lặp
    e.target.src = `${BASE}${id}.png?t=${Date.now()}`;
    return;
  }

  // Nếu PNG cũng fail → fallback theo giới tính
  e.target.src = fallbackAvatar(gender);
}
