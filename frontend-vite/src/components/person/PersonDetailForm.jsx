// ======================================================================
// File: src/components/PersonDetailForm.jsx (v3.3-LunarAuto-MobileSimple-FINAL)
// Mô tả tính năng:
//   ✔ Nhóm giao diện đơn giản – mobile-first
//   ✔ Ngày Âm tự động convert từ ngày DƯƠNG (birth_date, death_date)
//   ✔ Không hiển thị lại ngày dương ở Form Detail (đã có trong Form Basic)
//   ✔ anniversary_death nhập tay
//   ✔ Chia nhóm: Personal, Contact, Lunar Dates, Funeral, Admin
// ======================================================================

import React, { useState, useEffect } from "react";
import { getPersonDetail, updatePersonDetail } from "../../api/personDetailApi";
import { convertSolarToLunar } from "../../api/dateApi";

export default function PersonDetailForm({ personId, role }) {
  const [form, setForm] = useState({
    // PERSONAL INFO
    birth_place: "",
    nationality: "",
    ethnic_group: "",
    religion: "",
    languages_spoken: "",

    // CONTACT + EDUCATION
    address: "",
    phone_number: "",
    email: "",
    school_attended: "",
    degree_earned: "",

    // LUNAR DATES (AUTO)
    asian_birth_date: "",
    asian_death_date: "",
    anniversary_death: "",

    // FUNERAL
    death_place: "",
    grave_info: "",

    // ADMIN ONLY
    lineage_id: "",
    full_name_vn: "",
    blood_code: "",

    notes: "",
  });

  // ============================================================
  //  LOAD DETAIL
  // ============================================================
  useEffect(() => {
    loadDetail();
  }, [personId]);

  const loadDetail = async () => {
    try {
      const data = await getPersonDetail(personId);

      setForm((prev) => ({
        ...prev,
        ...data,
      }));

      // AUTO-CONVERT LUNAR
      // ---------------------------------------------------------
      if (data.birth_date) {
        try {
          const lunar = await convertSolarToLunar(data.birth_date);
          setForm((prev) => ({ ...prev, asian_birth_date: lunar }));
        } catch (e) {
          console.log("⚠ Không convert được ngày sinh âm");
        }
      }

      if (data.death_date) {
        try {
          const lunar = await convertSolarToLunar(data.death_date);
          setForm((prev) => ({ ...prev, asian_death_date: lunar }));
        } catch (e) {
          console.log("⚠ Không convert được ngày mất âm");
        }
      }
    } catch (err) {
      console.error("❌ Lỗi load detail:", err);
    }
  };

  // ============================================================
  // HANDLE CHANGE
  // ============================================================
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  // ============================================================
  //  SUBMIT
  // ============================================================
  const handleSubmit = async () => {
    try {
      await updatePersonDetail(personId, form);
      alert("✔ Cập nhật chi tiết thành công!");
    } catch (err) {
      console.error("❌ ERROR update:", err);
      alert("Không thể lưu thông tin chi tiết!");
    }
  };

  // ============================================================
  //  CARD WRAPPER
  // ============================================================
  const Card = ({ icon, title, children }) => (
    <div className="border rounded-lg p-4 shadow mb-6 bg-white">
      <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
        <span>{icon}</span> {title}
      </h3>
      {children}
    </div>
  );

  // ============================================================
  //  UI RENDER
  // ============================================================
  return (
    <div className="mt-6">

      {/* ============================
          PERSONAL INFORMATION
      ============================== */}
      <Card icon="📌" title="Thông Tin Cá Nhân">
        <div className="grid gap-3">
          <input name="birth_place" value={form.birth_place || ""} onChange={handleChange} placeholder="Nơi sinh" className="border p-2 rounded" />
          <input name="nationality" value={form.nationality || ""} onChange={handleChange} placeholder="Quốc tịch" className="border p-2 rounded" />
          <input name="ethnic_group" value={form.ethnic_group || ""} onChange={handleChange} placeholder="Dân tộc" className="border p-2 rounded" />
          <input name="religion" value={form.religion || ""} onChange={handleChange} placeholder="Tôn giáo" className="border p-2 rounded" />
          <input name="languages_spoken" value={form.languages_spoken || ""} onChange={handleChange} placeholder="Ngôn ngữ" className="border p-2 rounded" />
        </div>
      </Card>

      {/* ============================
          CONTACT + EDUCATION
      ============================== */}
      <Card icon="📞" title="Liên Hệ & Học Vấn">
        <div className="grid gap-3">
          <input name="address" value={form.address || ""} onChange={handleChange} placeholder="Địa chỉ" className="border p-2 rounded" />
          <input name="phone_number" value={form.phone_number || ""} onChange={handleChange} placeholder="Số điện thoại" className="border p-2 rounded" />
          <input name="email" value={form.email || ""} onChange={handleChange} placeholder="Email" className="border p-2 rounded" />
          <input name="school_attended" value={form.school_attended || ""} onChange={handleChange} placeholder="Trường học" className="border p-2 rounded" />
          <input name="degree_earned" value={form.degree_earned || ""} onChange={handleChange} placeholder="Bằng cấp" className="border p-2 rounded" />
        </div>
      </Card>

      {/* ============================
          LUNAR DATES
      ============================== */}
      <Card icon="📅" title="Ngày Tháng Âm Lịch">
        <div className="grid gap-3">
          <input value={form.asian_birth_date || ""} readOnly placeholder="Ngày sinh âm lịch" className="border p-2 rounded bg-gray-100" />
          <input value={form.asian_death_date || ""} readOnly placeholder="Ngày mất âm lịch" className="border p-2 rounded bg-gray-100" />
          <input name="anniversary_death" value={form.anniversary_death || ""} onChange={handleChange} placeholder="Ngày giỗ (dd/mm âm)" className="border p-2 rounded" />
        </div>
      </Card>

      {/* ============================
          FUNERAL
      ============================== */}
      <Card icon="⚰️" title="Thông Tin Tang Lễ">
        <div className="grid gap-3">
          <input name="death_place" value={form.death_place || ""} onChange={handleChange} placeholder="Nơi mất" className="border p-2 rounded" />
          <input name="grave_info" value={form.grave_info || ""} onChange={handleChange} placeholder="Thông tin mộ phần" className="border p-2 rounded" />
        </div>
      </Card>

      {/* ============================
          ADMIN SECTION
      ============================== */}
      {(role === "co_operator" || role === "admin") && (
        <Card icon="🛠" title="Admin / Điều Hành">
          <div className="grid gap-3">
            <input name="lineage_id" value={form.lineage_id || ""} onChange={handleChange} placeholder="Lineage ID" className="border p-2 rounded" />
            <input name="full_name_vn" value={form.full_name_vn || ""} onChange={handleChange} placeholder="Tên đầy đủ (VN)" className="border p-2 rounded" />
            <input name="blood_code" value={form.blood_code || ""} onChange={handleChange} placeholder="Blood Code" className="border p-2 rounded" />
          </div>
        </Card>
      )}

      {/* ============================
          NOTES
      ============================== */}
      <Card icon="📝" title="Ghi chú">
        <textarea
          name="notes"
          value={form.notes || ""}
          onChange={handleChange}
          className="border p-2 rounded w-full h-28"
          placeholder="Ghi chú thêm..."
        />
      </Card>

      {/* SAVE BUTTON */}
      <button onClick={handleSubmit} className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded shadow">
        💾 Lưu Thông Tin Chi Tiết
      </button>
    </div>
  );
}
