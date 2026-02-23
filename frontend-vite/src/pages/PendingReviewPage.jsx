// ======================================================================
// File: src/pages/PendingReviewPage.jsx (v2.0 - Workflow Ready)
// Mô tả:
//   - Xem chi tiết pending
//   - Chỉnh sửa dữ liệu before approve
//   - Approve → tạo 1 person mới → mở FormEdit
//   - Cancel approve
//   - Delete pending
// ======================================================================

import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import {
  getPendingDetail,
  updatePending,
  approvePending,
  cancelPending,
  deletePending,
} from "../api/pendingApi";

export default function PendingReviewPage({ role }) {
  const { id } = useParams();
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [form, setForm] = useState({});

  // -------------------------------------------------------------
  // Load pending detail
  // -------------------------------------------------------------
  useEffect(() => {
    async function load() {
      try {
        const res = await getPendingDetail(id);
        setData(res);
        setForm(res); // fill form
      } catch (err) {
        console.error("❌ Lỗi load pending:", err);
      }
    }
    load();
  }, [id]);

  // -------------------------------------------------------------
  // Cập nhật dữ liệu form
  // -------------------------------------------------------------
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // -------------------------------------------------------------
  // Lưu chỉnh sửa
  // -------------------------------------------------------------
  const handleSave = async () => {
    try {
      await updatePending(id, form);
      alert("✔ Đã cập nhật pending");
    } catch (err) {
      alert("❌ Không thể cập nhật");
      console.error(err);
    }
  };

  // -------------------------------------------------------------
  // Duyệt pending
  // -------------------------------------------------------------
  const handleApprove = async () => {
    if (!window.confirm("✔ Duyệt và tạo thành viên mới?")) return;

    try {
      const res = await approvePending(id);
      alert("Duyệt thành công! Chuyển sang FormEdit để hoàn thiện.");
      navigate(`/person/basic/${res.person_id}`);
    } catch (err) {
      alert("❌ Không thể duyệt pending");
      console.error(err);
    }
  };

  // -------------------------------------------------------------
  // Hủy duyệt
  // -------------------------------------------------------------
  const handleCancel = async () => {
    if (!window.confirm("↩ Hủy duyệt pending này?")) return;

    try {
      await cancelPending(id);
      alert("↩ Đã hủy duyệt, trả về waiting");
      navigate("/pending");
    } catch (err) {
      console.error(err);
      alert("❌ Không thể hủy duyệt");
    }
  };

  // -------------------------------------------------------------
  // Xóa pending
  // -------------------------------------------------------------
  const handleDelete = async () => {
    if (!window.confirm("🗑 Xóa pending này?")) return;

    try {
      await deletePending(id);
      alert("🗑 Đã xóa pending");
      navigate("/pending");
    } catch (err) {
      alert("❌ Không thể xóa");
      console.error(err);
    }
  };

  // -------------------------------------------------------------
  // Kiểm tra role
  // -------------------------------------------------------------
  if (role === "viewer" || role === "member_basic") {
    return (
      <div className="p-4 text-center text-red-500 font-bold">
        🚫 Bạn không có quyền xem trang này
      </div>
    );
  }

  if (!data) {
    return <div className="p-4 italic text-gray-600">Đang tải...</div>;
  }

  // -------------------------------------------------------------
  // Render form
  // -------------------------------------------------------------
  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-blue-700 mb-4">
        📄 Pending Review — {data.last_name} {data.middle_name} {data.first_name}
      </h2>

      <div className="grid grid-cols-2 gap-4">

        <div>
          <label className="font-semibold">Họ</label>
          <input
            name="last_name"
            value={form.last_name || ""}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>

        <div>
          <label className="font-semibold">Tên đệm</label>
          <input
            name="middle_name"
            value={form.middle_name || ""}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>

        <div>
          <label className="font-semibold">Tên</label>
          <input
            name="first_name"
            value={form.first_name || ""}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>

        <div>
          <label className="font-semibold">Giới tính</label>
          <select
            name="gender"
            value={form.gender || ""}
            onChange={handleChange}
            className="border p-2 w-full"
          >
            <option value="male">Nam</option>
            <option value="female">Nữ</option>
            <option value="other">Khác</option>
          </select>
        </div>

        <div>
          <label className="font-semibold">Ngày sinh</label>
          <input
            type="date"
            name="birth_date"
            value={form.birth_date || ""}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>

        <div>
          <label className="font-semibold">Ngày mất</label>
          <input
            type="date"
            name="death_date"
            value={form.death_date || ""}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>

        <div className="col-span-2">
          <label className="font-semibold">Lý do</label>
          <textarea
            name="reason"
            value={form.reason || ""}
            onChange={handleChange}
            className="border p-2 w-full h-24"
          ></textarea>
        </div>

      </div>

      {/* BUTTONS */}
      <div className="flex gap-3 mt-6">
        <button
          onClick={handleSave}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          💾 Lưu
        </button>

        <button
          onClick={handleApprove}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
        >
          ✔ Duyệt
        </button>

        <button
          onClick={handleCancel}
          className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded"
        >
          ↩ Hủy duyệt
        </button>

        <button
          onClick={handleDelete}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded"
        >
          🗑 Xóa
        </button>

      </div>
    </div>
  );
}
