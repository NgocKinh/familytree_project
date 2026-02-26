// src/api/apiConfig.js
// ===============================
// 🔹 Cấu hình API dùng chung cho toàn project
// ===============================

// Tự động nhận môi trường (development / production)
export const isDev = import.meta.env.MODE === "development";

// Backend URLs
export const API_FLASK = "http://localhost:5000/api";
export const API_FASTAPI = "http://localhost:8010/api";

// Tạm thời mặc định vẫn dùng Flask
export const API_BASE_URL = API_FLASK;

// Hàm tiện ích để tạo URL động (nếu muốn)
export const makeApiUrl = (endpoint) =>
  `${API_BASE_URL}${endpoint.startsWith("/") ? endpoint : `/${endpoint}`}`;


