import axios from "axios";
import { API_BASE_URL } from "./apiConfig";

const PARENT_CHILD_URL = `${API_BASE_URL}/parent_child`;

// ===============================
// 🔹 GET ALL: Lấy toàn bộ quan hệ cha–con
// ===============================
export const getParentChildList = async () => {
  const res = await axios.get(PARENT_CHILD_URL);
  return res.data;
};

// ===============================
// 🔹 GET ONE: Lấy quan hệ cha–con theo ID
// ===============================
export const getParentChildById = async (id) => {
  const res = await axios.get(`${PARENT_CHILD_URL}/${id}`);
  return res.data;
};

// ===============================
// 🔹 POST: Thêm quan hệ cha–con mới
// ===============================
export const addParentChild = async (data) => {
  const res = await axios.post(PARENT_CHILD_URL, data);
  return res.data;
};

// ===============================
// 🔹 PUT: Cập nhật quan hệ cha–con theo ID
// ===============================
export const updateParentChild = async (id, data) => {
  const res = await axios.put(`${PARENT_CHILD_URL}/${id}`, data);
  return res.data;
};

// ===============================
// 🔹 DELETE: Xóa quan hệ cha–con theo ID
// ===============================
export const deleteParentChild = async (id) => {
  const res = await axios.delete(`${PARENT_CHILD_URL}/${id}`);
  return res.data;
};
