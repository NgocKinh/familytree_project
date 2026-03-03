// =======================================================
// File: src/api/personApi.js (v6.5-PRO-DONG-BO-AVATAR-FINAL)
// Mô tả:
//   - Đồng bộ tuyệt đối với backend (person_api.py + avatar_api.py)
//   - Giữ nguyên 100% các route đang dùng trong dự án
//   - Thêm comment rõ ràng, format sạch, không đổi logic
// =======================================================

import axios from "axios";
import { API_FASTAPI } from "./apiConfig";
console.log("API_FASTAPI =", API_FASTAPI);
// ============================================
// BASE URL (KHÔNG ĐƯỢC ĐỔI nếu backend giữ nguyên)
// ============================================
const PERSON_URL = `${API_FASTAPI}/api/person/basic`;
const API_URL    = `${API_FASTAPI}/person`;
const AVATAR_URL = `${API_FASTAPI}/avatar/upload`;

// ============================================
// LẤY DANH SÁCH PERSON
// ============================================
export const getPersonList = async () => {
  try {
    const res = await axios.get(PERSON_URL);
    return res.data; // luôn là array []
  } catch (err) {
    console.error("❌ Lỗi khi lấy danh sách:", err);
    throw err;
  }
};

// Alias cũ
export const getAllPersons = getPersonList;

// ============================================
// SOFT DELETE (ẨN TẠM)
// ============================================
export const softDeletePerson = (id) =>
  axios.put(`${API_URL}/delete_soft/${id}`);

// ============================================
// RESTORE (PHỤC HỒI)
// ============================================
export const restorePerson = (id) =>
  axios.put(`${API_URL}/restore/${id}`);

// ============================================
// HARD DELETE (XÓA VĨNH VIỄN – ADMIN)
// ============================================
export const hardDeletePerson = (id) =>
  axios.delete(`${API_URL}/delete_permanent/${id}`);

// ============================================
// GET: LẤY CHI TIẾT PERSON (FORM BASIC / FORM DETAIL)
// ============================================
export const getPersonById = async (id) => {
  try {
    const res = await axios.get(`${API_URL}/basic/${id}`);
    return res.data;
  } catch (err) {
    console.error(`❌ Lỗi khi lấy chi tiết ID=${id}:`, err);
    throw err;
  }
};

// ============================================
// POST: THÊM PERSON (FORM BASIC)
// ============================================
export const addPerson = async (data) => {
  try {
    const res = await axios.post(`${API_URL}/basic`, data, {
      headers: { "Content-Type": "application/json" },
    });
    return res.data;
  } catch (err) {
    console.error("❌ Lỗi thêm người mới:", err);
    throw err;
  }
};

// ============================================
// PUT: CẬP NHẬT PERSON
// ============================================
export const updatePerson = async (id, data) => {
  try {
    const res = await axios.put(`${API_URL}/basic/${id}`, data, {
      headers: { "Content-Type": "application/json" },
    });
    return res.data;
  } catch (err) {
    console.error(`❌ Lỗi cập nhật ID=${id}:`, err);
    throw err;
  }
};

// ============================================
// CHECK DUPLICATE
// ============================================
export const checkDuplicatePerson = async (data) => {
  const res = await axios.post(`${API_URL}/check_duplicate`, data);
  return res.data;
};

// ======================================================================
// 🔵 UPLOAD AVATAR
// ======================================================================
export const uploadAvatar = async (personId, file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await axios.post(`${AVATAR_URL}/${personId}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    return res.data; // filename + message
  } catch (err) {
    console.error("❌ Lỗi upload avatar:", err);
    throw err;
  }
};
