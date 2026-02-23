// ======================================================================
// File: PersonSelectWithAvatarV2.jsx (v2.0-FINAL)
// Mô tả:
//   - Dropdown avatar đẹp (28px), popup gọn
//   - Toggle lọc giới tính kiểu iOS
//   - Auto bật khi người chọn có giới tính phù hợp
//   - Người dùng vẫn có thể tắt để xem toàn bộ
//   - Tương thích avatarEngine (JPG → PNG → default)
// ======================================================================

import React, { useState, useRef, useEffect } from "react";
import { getAvatarURL, handleAvatarError } from "../../utils/avatarEngine";

export default function PersonSelectWithAvatarV2({
  label = "",
  value = "",
  onChange,
  persons = [],
  genderFilter,
}) {
  const [open, setOpen] = useState(false);
  const [filterOn, setFilterOn] = useState(true); // trạng thái toggle
  const ref = useRef();

  const effectiveGender =
    genderFilter ??
    (label.includes("Chồng") ? "male" :
      label.includes("Vợ") ? "female" :
        null);
  // Sync trạng thái toggle khi mở component
  useEffect(() => {
    if (effectiveGender) {
      setFilterOn(true);   // có giới tính → bật toggle
    } else {
      setFilterOn(false);  // không có → tắt
    }
  }, [effectiveGender]);

  // Đóng popup khi click ra ngoài
  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const selected = persons.find((p) => String(p.person_id) === String(value));

  // ==========================================
  // AUTO BẬT FILTER NẾU NGƯỜI ĐƯỢC CHỌN TRÙNG GIỚI TÍNH
  // ==========================================
  useEffect(() => {
    if (!selected) return;
    if (!genderFilter) return; // không áp dụng

    if (selected.gender === genderFilter) {
      setFilterOn(true); // auto bật
    }
  }, [selected, genderFilter]);

  // ==========================================
  // Lọc danh sách theo toggle
  // ==========================================
  const filteredPersons = persons.filter((p) => {
    if (filterOn && effectiveGender) {
      return p.gender === effectiveGender;
    }
    return true;
  });

  // ==========================================
  // Format tên: Fullname + lifespan
  // ==========================================
  const formatPersonName = (p) => {
    const fullname =
      p.full_name_vn ||
      [p.last_name, p.middle_name, p.first_name].filter(Boolean).join(" ");

    const birth = p.birth_date ? p.birth_date.slice(0, 4) : "";
    const death = p.death_date ? p.death_date.slice(0, 4) : "";

    return `${fullname} (${birth || " "}–${death || " "})`;
  };

  return (
    <div className="mb-4 relative" ref={ref}>
      {/* LABEL */}
      <label className="block mb-1 font-semibold text-gray-700">{label}</label>

      {/* TOGGLE FILTER */}
      <div className="flex items-center space-x-2 mb-1">
        {/* Switch iOS Style */}
        <div
          onClick={() => setFilterOn(!filterOn)}
          className={`w-10 h-5 flex rounded-full cursor-pointer transition ${filterOn ? "bg-blue-600" : "bg-gray-300"
            }`}
        >
          <div
            className={`h-5 w-5 bg-white rounded-full shadow transform transition ${filterOn ? "translate-x-5" : "translate-x-0"
              }`}
          />
        </div>

        <span className="text-gray-700 text-sm">
          {effectiveGender === "male"
            ? "Chỉ hiện người giới tính Nam"
            : effectiveGender === "female"
              ? "Chỉ hiện người giới tính Nữ"
              : "Chỉ hiện theo giới tính"}
        </span>
      </div>

      {/* SELECTED BOX */}
      <div
        onClick={() => setOpen(!open)}
        className="border rounded px-2 py-2 flex items-center space-x-2 cursor-pointer bg-white hover:bg-gray-50"
      >
        {selected ? (
          <>
            <img
              src={getAvatarURL(selected.person_id, selected.gender)}
              onError={(e) =>
                handleAvatarError(e, selected.person_id, selected.gender)
              }
              className="w-7 h-7 rounded-full object-cover"
            />
            <span>{formatPersonName(selected)}</span>
          </>
        ) : (
          <span className="text-gray-400">-- Chọn người --</span>
        )}
      </div>

      {/* POPUP */}
      {open && (
        <div className="absolute mt-1 border rounded shadow bg-white max-h-60 overflow-y-auto w-full z-50">

          {filteredPersons.map((p) => (
            <div
              key={p.person_id}
              onClick={() => {
                onChange(String(p.person_id));
                setOpen(false);
              }}
              className="flex items-center space-x-2 p-2 cursor-pointer hover:bg-gray-100"
            >
              <img
                src={getAvatarURL(p.person_id, p.gender)}
                onError={(e) => handleAvatarError(e, p.person_id, p.gender)}
                className="w-7 h-7 rounded-full object-cover"
              />
              <span>{formatPersonName(p)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
