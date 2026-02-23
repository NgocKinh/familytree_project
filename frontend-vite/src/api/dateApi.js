// ======================================================================
// File: src/api/dateApi.js  (v1.1-FIXED)
// ======================================================================

import axios from "axios";

const API_BASE = "http://127.0.0.1:5000/api";

// 🔹 Convert solar → lunar using backend Flask API
export async function convertSolarToLunar(solarDate) {
  if (!solarDate) return "";

  try {
    const res = await axios.post(`${API_BASE}/convert_lunar`, {
      birth_date: solarDate,
    });

    return res.data.lunar_date || "";
  } catch (err) {
    console.error("❌ convertSolarToLunar ERROR:", err);
    return "";
  }
}