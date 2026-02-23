// src/api/apiConfig.js
// ===============================
// 🔹 Cấu hình API dùng chung cho toàn project
// ===============================

// Tự động nhận môi trường (development / production)
export const isDev = import.meta.env.MODE === "development";

// URL gốc của backend Flask
export const API_BASE_URL = isDev
  ? "http://localhost:5000/api"
  : "https://your-domain.com/api"; // ⚠️ sửa lại khi deploy

// Hàm tiện ích để tạo URL động (nếu muốn)
export const makeApiUrl = (endpoint) =>
  `${API_BASE_URL}${endpoint.startsWith("/") ? endpoint : `/${endpoint}`}`;


