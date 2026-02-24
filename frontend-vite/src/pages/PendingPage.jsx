// ======================================================================
// File: src/pages/PendingPage.jsx (v2.0 - Workflow Ready)
// Mô tả:
//   - Hiển thị danh sách chờ duyệt (pending)
//   - Dùng API mới pendingApi.js
//   - Có nút xem chi tiết / duyệt / xóa
// ======================================================================

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getPendingList,
  approvePending,
  deletePending,
} from "../api/pendingApi";

import { getAvatarURL } from "../utils/avatarEngine";
export default function PendingPage({ role }) {
  const navigate = useNavigate();
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);

  // -------------------------------------------------------------
  // Tải danh sách pending
  // -------------------------------------------------------------
  const loadData = async () => {
    try {
      setLoading(true);
      const data = await getPendingList();
      setList(data);
    } catch (err) {
      console.error("❌ Lỗi load pending:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // -------------------------------------------------------------
  // Action: Xem chi tiết pending
  // -------------------------------------------------------------
  const handleView = (id) => {
    navigate(`/pending/review/${id}`);
  };

  // -------------------------------------------------------------
  // Action: Duyệt pending
  // -------------------------------------------------------------
  const handleApprove = async (id) => {
    if (!window.confirm("✔ Duyệt thành viên này?")) return;
    try {
      const res = await approvePending(id);
      alert("Duyệt thành công! Chuyển sang FormEdit để hoàn thiện.");
      navigate(`/person/basic/${res.person_id}`); // mở FormEdit
    } catch (err) {
      console.error("❌ Lỗi duyệt:", err);
      alert("Không thể duyệt pending!");
    }
  };

  // -------------------------------------------------------------
  // Action: Xóa pending
  // -------------------------------------------------------------
  const handleDelete = async (id) => {
    if (!window.confirm("🗑 Xóa pending này?")) return;
    try {
      await deletePending(id);
      loadData();
    } catch (err) {
      console.error("❌ Lỗi xóa pending:", err);
    }
  };

  // -------------------------------------------------------------
  // Kiểm tra role
  // -------------------------------------------------------------
  if (role === "viewer" || role === "member_basic") {
    return (
      <div className="p-4 text-center text-red-500 font-bold">
        🚫 Bạn không có quyền xem danh sách chờ duyệt
      </div>
    );
  }

  // -------------------------------------------------------------
  // Render
  // -------------------------------------------------------------
  return (
    <div className="p-4">
      <h2 className="text-2xl mb-4 font-bold text-blue-700">
        📥 Danh sách chờ duyệt
      </h2>

      {loading ? (
        <div className="italic text-gray-500">Đang tải...</div>
      ) : list.length === 0 ? (
        <div className="italic text-gray-500">Không có bản ghi chờ duyệt</div>
      ) : (
        <table className="min-w-full border border-gray-300">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-2">Ảnh</th>
              <th className="px-4 py-2">Họ tên</th>
              <th className="px-4 py-2">Giới tính</th>
              <th className="px-4 py-2">Ngày tạo</th>
              <th className="px-4 py-2 text-center">Hành động</th>
            </tr>
          </thead>

          <tbody>
            {list.map((p) => (
              <tr key={p.pending_id} className="border-t hover:bg-gray-50">
                <td className="px-4 py-2 text-center">
                  <img
                    src={getAvatarURL(p.person_id, p.gender)}
                    className="w-12 h-12 mx-auto rounded-full object-cover border"
                  />
                </td>

                <td className="px-4 py-2">
                  {`${p.last_name} ${p.middle_name ?? ""} ${p.first_name}`}
                </td>

                <td className="px-4 py-2">
                  {p.gender === "male"
                    ? "Nam"
                    : p.gender === "female"
                    ? "Nữ"
                    : "Khác"}
                </td>

                <td className="px-4 py-2">
                  {p.created_at ? p.created_at.substring(0, 10) : ""}
                </td>

                <td className="px-4 py-2 text-center space-x-2">
                  <button
                    onClick={() => handleView(p.pending_id)}
                    className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                  >
                    🔍 Xem
                  </button>

                  <button
                    onClick={() => handleApprove(p.pending_id)}
                    className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded"
                  >
                    ✔ Duyệt
                  </button>

                  <button
                    onClick={() => handleDelete(p.pending_id)}
                    className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded"
                  >
                    🗑 Xóa
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
