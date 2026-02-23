// ======================================================================
// File: MarriagePage.jsx (v11.0-Full-Optimized)
// Mô tả:
//   - 2 tab: Danh sách / Thêm - Sửa
//   - Khi bấm ✏️ từ danh sách → mở form và truyền editId
//   - Khi bấm Quay Lại → trở về danh sách
// ======================================================================

import React, { useState } from "react";
import MarriageList from "../components/MarriageList";
import MarriageForm from "../components/marriage/MarriageForm";

export default function MarriagePage() {
  const [activeTab, setActiveTab] = useState("list");
  const [editId, setEditId] = useState(null);

  // Khi bấm nút Sửa trong danh sách
  const handleEdit = (id) => {
    console.log("🟦 EDIT ID:", id);
    setEditId(id);
    setActiveTab("form");
  };

  // Khi lưu xong hoặc quay lại
  const handleBack = () => {
    setEditId(null);
    setActiveTab("list");
  };

  return (
    <div className="max-w-6xl mx-auto p-4 bg-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold text-center text-blue-600 mb-4">
        💍 Quản Lý Quan Hệ Hôn Nhân
      </h2>

      {/* Tabs */}
      <div className="flex justify-center gap-4 mb-6">
        <button
          onClick={handleBack}
          className={`px-4 py-2 rounded ${
            activeTab === "list"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-700"
          }`}
        >
          📋 Danh sách
        </button>

        <button
          onClick={() => {
            setEditId(null);
            setActiveTab("form");
          }}
          className={`px-4 py-2 rounded ${
            activeTab === "form"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-700"
          }`}
        >
          ✏️ Thêm / Sửa
        </button>
      </div>

      {/* Nội dung */}
      {activeTab === "list" ? (
        <MarriageList onEdit={handleEdit} />
      ) : (
        <MarriageForm editId={editId} onBack={handleBack} />
      )}
    </div>
  );
}
