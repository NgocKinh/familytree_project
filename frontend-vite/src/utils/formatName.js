/**
 * ✅ formatName.js (Final Ultimate Stable+ v2.1)
 * Giữ nguyên tương thích cũ + sửa chuẩn viết tắt "T. T. Lượng"
 */

export function formatName(person, mode = "full", options = {}) {
  if (!person) return "";

  const {
    showSurName = true,
    showYears = false,
    showId = false,
    showLineage = false,
  } = options;

  const sur = person.sur_name?.trim() || "";
  const last = person.last_name?.trim() || "";
  const mid = person.middle_name?.trim() || "";
  const first = person.first_name?.trim() || "";
  const fullFromDB = person.full_name_vn?.trim() || "";

  // ----------------------------
  // 1️⃣ Xác định họ tên chính
  // ----------------------------
  let name = "";
  if (fullFromDB && mode === "full") {
    name = fullFromDB;
  } else if (mode === "short") {
    // ✅ Viết tắt theo chuẩn học thuật: T. T. Lượng
    const lastShort = last ? last.charAt(0).toUpperCase() + "." : "";
    const midShort = mid ? mid.charAt(0).toUpperCase() + "." : "";
    name = [lastShort, midShort, first].filter(Boolean).join(" ");
  } else {
    name = [last, mid, first].filter(Boolean).join(" ");
  }

  // ----------------------------
  // 2️⃣ Ghép Tên hiệu – Họ tên (nếu bật)
  // ----------------------------
  if (showSurName && sur) {
    name = `${sur} – ${name}`;
  }

  // ----------------------------
  // 3️⃣ Thêm năm sinh – năm mất
  // ----------------------------
  if (showYears) {
    const birthYear = person.birth_date
      ? new Date(person.birth_date).getFullYear()
      : "?";
    const deathYear = person.death_date
      ? new Date(person.death_date).getFullYear()
      : "";
    name += ` (${birthYear}${deathYear ? "–" + deathYear : ""})`;
  }

  // ----------------------------
  // 4️⃣ Thêm ID nếu có
  // ----------------------------
  if (showId && person.person_id) {
    name += ` [ID: ${person.person_id}]`;
  }

  // ----------------------------
  // 5️⃣ Thêm họ tộc (nếu có)
  // ----------------------------
  if (showLineage && person.lineage_name) {
    name += ` (họ ${person.lineage_name})`;
  }

  return name.trim();
}

