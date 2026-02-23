// ======================================================
// File: src/api/treeApi.js
// ======================================================

import axios from "axios";

// ⚠️ Backend Flask – giữ nguyên
const API_BASE = "http://127.0.0.1:5000/api/tree/family";

export async function getFamilyTree(id) {
  if (!id) {
    throw new Error("ID is required");
  }

  try {
    const res = await axios.get(`${API_BASE}/${id}`);
    const data = res.data || {};

    // Chuẩn hoá dữ liệu cho TreePage
    return {
      center: data.center,
      spouse: data.spouse,
      marriage_status: data.marriage_status,
      father_parents: data.father_parents || [],
      mother_parents: data.mother_parents || [],
      children_common: data.children_common || [],
      children_father_separate: data.children_father_separate || [],
      children_mother_separate: data.children_mother_separate || [],
    };
  } catch (err) {
    console.error("❌ Lỗi API getFamilyTree:", err);
    throw err;
  }
}