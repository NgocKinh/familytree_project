// =============================================================
// File: src/api/personDetailApi.js (v1.5 – FULL, CLEAN, READY)
// Mô tả:
//   - Gọi API chi tiết thành viên
//   - Đồng bộ endpoint: /api/person/detail
//   - Hỗ trợ GET / POST / PUT
//   - Có alias getPersonDetail để PersonDetailForm dùng
// =============================================================

const BASE_URL = "http://127.0.0.1:5000/api/person/detail";

// -------------------------------------------------------------
// 🔹 Lấy chi tiết 1 person theo ID
// -------------------------------------------------------------
export async function getPersonDetailById(personId) {
  const res = await fetch(`${BASE_URL}/${personId}`);
  if (!res.ok) throw new Error("Không thể tải dữ liệu chi tiết");
  return res.json();
}

// -------------------------------------------------------------
// ⭐ Alias cho PersonDetailForm (đang gọi getPersonDetail)
// -------------------------------------------------------------
export const getPersonDetail = getPersonDetailById;

// -------------------------------------------------------------
// 🔹 Thêm mới chi tiết (ADD)
// -------------------------------------------------------------
export async function addPersonDetail(payload) {
  const res = await fetch(BASE_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) throw new Error("Không thể thêm chi tiết");
  return res.json();
}

// -------------------------------------------------------------
// 🔹 Cập nhật chi tiết (UPDATE)
// -------------------------------------------------------------
export async function updatePersonDetail(personId, payload) {
  const res = await fetch(`${BASE_URL}/${personId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) throw new Error("Không thể cập nhật chi tiết");
  return res.json();
}


