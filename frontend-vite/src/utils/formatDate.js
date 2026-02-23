/**
 * Utils: Xử lý ngày tháng theo chuẩn Việt Nam
 * - Dùng cho nhập liệu (parse) và hiển thị (format)
 * - Lưu DB theo ISO (yyyy-mm-dd), hiển thị VN (dd/mm/yyyy, mm/yyyy, yyyy)
 */

function normalizeInput(input) {
  if (input == null) return "";
  if (typeof input !== "string") input = String(input);
  return input.replace(/-/g, "/").trim();
}

/**
 * Định dạng ngày theo chuẩn VN để hiển thị
 * @param {string} dateStr - Chuỗi ngày (ISO, GMT hoặc dạng VN)
 * @param {string} precision - "year" | "month" | "exact"
 */
export function formatDateVN(dateStr, precision = "exact") {
  if (!dateStr) return "";

  // ✅ Nếu là ISO (yyyy-mm-dd) hoặc có dạng DateTime
  const match = dateStr.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (match) {
    const [_, y, m, d] = match;

    // Xử lý logic precision
    if (precision === "year" || (d === "01" && m === "01")) return y;
    if (precision === "month" || d === "01") return `${m}/${y}`;
    return `${d}/${m}/${y}`;
  }

  // ✅ Nếu là chuỗi GMT hoặc JS Date hợp lệ
  const jsDate = new Date(dateStr);
  if (!isNaN(jsDate.getTime())) {
    const d = String(jsDate.getDate()).padStart(2, "0");
    const m = String(jsDate.getMonth() + 1).padStart(2, "0");
    const y = jsDate.getFullYear();

    if (precision === "year" || (d === "01" && m === "01")) return y;
    if (precision === "month" || d === "01") return `${m}/${y}`;
    return `${d}/${m}/${y}`;
  }

  // ✅ Nếu người dùng nhập trực tiếp dạng dd/mm/yyyy, mm/yyyy, yyyy
  const normalized = normalizeInput(dateStr);
  return normalized;
}

/**
 * Xác định độ chính xác từ chuỗi người dùng nhập
 */
export function detectPrecision(input) {
  if (!input) return "unknown";
  const normalized = normalizeInput(input);

  if (/^\d{4}$/.test(normalized)) return "year";
  if (/^\d{1,2}\/\d{4}$/.test(normalized)) return "month";
  if (/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(normalized)) return "exact";
  return "unknown";
}

/**
 * Chuyển input người dùng (VN) về chuẩn ISO yyyy-mm-dd
 */
export function parseVNDate(input) {
  if (!input) return null;
  const normalized = normalizeInput(input);
  const parts = normalized.split("/");

  if (parts.length === 1) {
    const [y] = parts;
    return `${y}-01-01`; // yyyy
  } else if (parts.length === 2) {
    const [m, y] = parts;
    return `${y}-${m.padStart(2, "0")}-01`; // mm/yyyy
  } else if (parts.length === 3) {
    const [d, m, y] = parts;
    return `${y}-${m.padStart(2, "0")}-${d.padStart(2, "0")}`; // dd/mm/yyyy
  }
  return input;
}











