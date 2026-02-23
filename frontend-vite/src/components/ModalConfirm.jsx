// ============================================================
// File: src/components/ModalConfirm.jsx (v1.0-final)
// Mô tả:
//   - Modal xác nhận thao tác nguy hiểm (xóa vĩnh viễn, khôi phục...)
//   - Có thể tái sử dụng cho các hành động khác
// ============================================================

import React from "react";

const ModalConfirm = ({ show, title, message, onConfirm, onCancel }) => {
  if (!show) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-white rounded-2xl shadow-xl p-6 w-[400px] text-center">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">{title}</h2>
        <p className="text-gray-600 mb-6">{message}</p>

        <div className="flex justify-center gap-4">
          <button
            onClick={onCancel}
            className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 px-4 rounded-xl"
          >
            Hủy
          </button>
          <button
            onClick={onConfirm}
            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-xl"
          >
            Xác nhận
          </button>
        </div>
      </div>
    </div>
  );
};

export default ModalConfirm;
