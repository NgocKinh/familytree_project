import axios from "axios";
import { API_BASE_URL } from "./apiConfig";

const MARRIAGE_URL = `${API_BASE_URL}/marriage`;

// ===============================
// 🔹 GET ALL: Lấy toàn bộ quan hệ hôn nhân
// ===============================
export const getMarriageList = async () => {
  const res = await axios.get(MARRIAGE_URL);
  return res.data;
};

// ===============================
// 🔹 GET ONE: Lấy 1 quan hệ hôn nhân theo ID
// ===============================
export const getMarriageById = async (id) => {
  const res = await axios.get(`${MARRIAGE_URL}/${id}`);
  return res.data;
};

// ===============================
// 🔹 POST: Thêm quan hệ hôn nhân mới
// ===============================
export const addMarriage = async (data) => {
  const res = await axios.post(MARRIAGE_URL, data);
  return res.data;
};

// ===============================
// 🔹 PUT: Cập nhật quan hệ hôn nhân theo ID
// ===============================
export const updateMarriage = async (id, data) => {
  const res = await axios.put(`${MARRIAGE_URL}/${id}`, data);
  return res.data;
};

// ===============================
// 🔹 DELETE: Xóa quan hệ hôn nhân theo ID
// ===============================
export const deleteMarriage = async (id) => {
  const res = await axios.delete(`${MARRIAGE_URL}/${id}`);
  return res.data;
};
