// src/utils/format.js

/**
 * Hiển thị giới tính theo tiếng Việt
 * - male   → Nam
 * - female → Nữ
 * - other  → Khác
 * - null/unknown → ""
 */
export function formatGender(gender) {
  if (!gender) return "";
  const g = gender.toLowerCase();
  if (g === "male") return "Nam";
  if (g === "female") return "Nữ";
  if (g === "other") return "Khác";
  return "";
}

