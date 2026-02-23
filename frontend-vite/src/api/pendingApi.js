// =======================================================================
// File: src/api/pendingApi.js
// =======================================================================

const BASE = "http://127.0.0.1:5000/api/person_pending";

// 🟦 1) Lấy danh sách pending
export async function getPendingList() {
  const res = await fetch(BASE);
  if (!res.ok) throw new Error("Không lấy được danh sách pending");
  return await res.json();
}

// 🟦 2) Lấy chi tiết 1 pending
export async function getPendingDetail(id) {
  const res = await fetch(`${BASE}/${id}`);
  if (!res.ok) throw new Error("Không lấy được chi tiết pending");
  return await res.json();
}

// 🟩 3) Cập nhật pending
export async function updatePending(id, payload) {
  const res = await fetch(`${BASE}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Không cập nhật được pending");
  return await res.json();
}

// 🟩 4) Duyệt pending
export async function approvePending(id) {
  const res = await fetch(`${BASE}/approve/${id}`, { method: "PUT" });
  if (!res.ok) throw new Error("Không duyệt được pending");
  return await res.json();
}

// 🟥 5) Hủy duyệt
export async function cancelPending(id) {
  const res = await fetch(`${BASE}/cancel/${id}`, { method: "PUT" });
  if (!res.ok) throw new Error("Không thể hủy duyệt");
  return await res.json();
}

// 🗑 6) Xóa pending
export async function deletePending(id) {
  const res = await fetch(`${BASE}/delete/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Không thể xóa pending");
  return await res.json();
}
