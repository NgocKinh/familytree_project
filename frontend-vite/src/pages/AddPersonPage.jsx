// ======================================================================
// File: src/pages/AddPersonPage.jsx (v6.5-FINAL-FixDetailRender)
// Mô tả cập nhật v6.5:
//   - Đồng bộ hoàn toàn với PersonBasicForm v7.6
//   - Đảm bảo Form Detail xuất hiện khi EDIT và CREATE
//   - Sửa lỗi callback không nhận được ID từ FormBasic
//   - Giữ nguyên logic phân quyền
// ======================================================================

import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import PersonBasicForm from "../components/person/PersonBasicForm";
import PersonDetailForm from "../components/person/PersonDetailForm";

export default function AddPersonPage({ role }) {
  const { id } = useParams();

  const isEditMode = Boolean(id);

  // ==============================================
  // QUẢN LÝ ID VÀ TRẠNG THÁI FORM DETAIL
  // ==============================================
  const [personId, setPersonId] = useState(id || null);
  const [showDetailForm, setShowDetailForm] = useState(false);

  // Ai được phép xem Form Chi Tiết?
  const canShowDetail =
    role === "member_close" ||
    role === "co_operator" ||
    role === "admin";

  // ======================================================================
  // Khi mở trang ở chế độ EDIT → tự động hiển thị Form Detail
  // ======================================================================
  useEffect(() => {
    if (isEditMode && canShowDetail) {
      // ✅ [CHANGE 1]: Luôn set lại personId khi mở trang edit
      setPersonId(id);
      setShowDetailForm(true);
    }
  }, [isEditMode, id, canShowDetail]);

  // ======================================================================
  // Callback từ PersonBasicForm (khi lưu xong)
  // ======================================================================
  const handleSavedBasic = (result) => {
    // Backend có thể trả id hoặc person_id → chuẩn hoá
    // ----------------------------------------------------------
    // result = { id: 10, ... } hoặc { person_id: 10, ... }
    // ----------------------------------------------------------

    const savedId =
      result?.id ||
      result?.person_id ||
      id; // fallback khi đang edit

    // Nếu không lấy được ID → không thể render Form Detail
    if (!savedId) return;

    // Lưu ID vào state
    setPersonId(savedId);

    // ==================================================================
    // Quy tắc hiển thị Form Detail:
    // - member_close trở lên → luôn hiển thị
    // - member_basic → không hiển thị
    // ==================================================================
    if (canShowDetail) {
      // ✅ [CHANGE 2]: Hiển thị form chi tiết NGAY SAU KHI LƯU
      setShowDetailForm(true);
    }
  };

  // ======================================================================
  // GIAO DIỆN CHÍNH
  // ======================================================================
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4 text-center">
        {isEditMode ? "✏️ Sửa Thành Viên" : "➕ Thêm Thành Viên"}
      </h2>

      {/* FORM CƠ BẢN */}
      <PersonBasicForm role={role} onSaved={handleSavedBasic} />

      {/* FORM CHI TIẾT */}
      {canShowDetail && showDetailForm && personId && (
        <div className="mt-8 border-t pt-6">
          {/*  ✅ [CHANGE 3]: Truyền đúng personId đã chuẩn hoá */}
          <PersonDetailForm personId={personId} role={role} />
        </div>
      )}
    </div>
  );
}
