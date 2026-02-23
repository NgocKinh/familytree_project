// src/pages/PersonEditPage.jsx
import React from "react";
import { useParams } from "react-router-dom";

function PersonEditPage() {
  const { id } = useParams();

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Chỉnh sửa thành viên</h1>
      <p className="mb-4">Bạn đang chỉnh sửa thành viên có ID: <b>{id}</b></p>

      {/* Placeholder form */}
      <form className="space-y-4">
        <div>
          <label className="block mb-1 font-medium">Tên chính</label>
          <input
            type="text"
            placeholder="Nhập tên chính..."
            className="w-full border px-3 py-2 rounded"
            disabled
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">Ngày sinh</label>
          <input
            type="date"
            className="w-full border px-3 py-2 rounded"
            disabled
          />
        </div>
        <button
          type="button"
          className="bg-gray-400 text-white px-4 py-2 rounded"
          disabled
        >
          (Placeholder) Lưu chỉnh sửa
        </button>
      </form>
    </div>
  );
}

export default PersonEditPage;
