// ===================================================================
// personBasicApi.js (v3.0-CLEAN-FINAL)
// - Trả về danh sách thành viên đầy đủ từ backend
// - Dùng chung cho ParentChildForm, MarriageForm, RelationFinder
// - API CHUẨN: /api/person/
// ===================================================================
import axios from "axios";
import { API_BASE_URL } from "./apiConfig";

const PERSON_URL = `${API_BASE_URL}/person/basic`;

export const getPersonBasicList = async () => {
  try {
    const res = await axios.get(PERSON_URL); 
    return res.data || [];
  } catch (err) {
    console.error("❌ Lỗi tải danh sách cơ bản:", err);
    return [];
  }
};


// ===================================================================
// 🔹 GET theo ID
// ===================================================================
export const getPersonBasicById = async (id) => {
  try {
    // ✅ [CHANGE 2]: thêm await (file gốc của bạn bị thiếu)
    const res = await axios.get(`${PERSON_URL}/${id}`);

    return res.data;
  } catch (err) {
    console.error("❌ Lỗi tải chi tiết person:", err);
    throw err;
  }
};


// ===================================================================
// 🔹 POST: thêm mới
// ===================================================================
export const addPersonBasic = async (personData) => {
  try {
    const res = await axios.post(`${PERSON_URL}/`, personData); 
    //       🔵 [ADDED 2] thêm "/" để backend nhận dạng POST đúng
    
    return res.data;
  } catch (err) {
    console.error("❌ Lỗi thêm person:", err);
    throw err;
  }
};


// ===================================================================
// 🔹 PUT: cập nhật
// ===================================================================
export const updatePersonBasic = async (id, personData) => {
  try {
    const res = await axios.put(`${PERSON_URL}/${id}`, personData);
    // 👍 Route này đúng, không thêm "/"

    return res.data;
  } catch (err) {
    console.error("❌ Lỗi cập nhật person:", err);
    throw err;
  }
};


// ===================================================================
// 🔹 DELETE
// ===================================================================
export const deletePersonBasic = async (id) => {
  try {
    const res = await axios.delete(`${PERSON_URL}/${id}`);
    return res.data;
  } catch (err) {
    console.error("❌ Lỗi xóa person:", err);
    throw err;
  }
};


