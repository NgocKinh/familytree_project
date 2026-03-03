// ======================================================================
// File: MarriageList.jsx (v11.0-Optimized)
// Mô tả:
//   - Hiển thị danh sách hôn nhân
//   - Full / Short Name + SurName
//   - Nhấn ✏️ truyền id sang MarriagePage → MarriageForm
// ======================================================================

import React, { useEffect, useState } from "react";
import axios from "axios";
import { formatDateVN } from "../utils/formatDate";

const API_BASE = "http://127.0.0.1:8010/api";

export default function MarriageList({ onEdit }) {
  const [marriages, setMarriages] = useState([]);
  const [mode, setMode] = useState("full");
  const [showSurName, setShowSurName] = useState(false);
  const [deleteConfirmId, setDeleteConfirmId] = useState(null);
  const [message, setMessage] = useState("");

  // ================================================================
  // LOAD
  // ================================================================
  const fetchMarriages = async () => {
    try {
      const res = await axios.get(`${API_BASE}/marriage`);
      setMarriages(res.data || []);
    } catch (err) {
      setMessage("❌ Không tải được danh sách hôn nhân!");
    }
  };

  useEffect(() => {
    fetchMarriages();
  }, []);

  // ================================================================
  // Tên đầy đủ / rút gọn
  // ================================================================
  const abbreviateName = (p) => {
    const initials = [p.last_name, p.middle_name]
      .filter(Boolean)
      .map((x) => x.trim()[0]?.toUpperCase() + ".")
      .join(" ");
    return `${initials} ${p.first_name}`.trim();
  };

  const buildDisplayName = (rawName, surName) => {
    if (!rawName) return "";

    const split = rawName.split("|");
    const p = {
      last_name: split[0] || "",
      middle_name: split[1] || "",
      first_name: split[2] || "",
    };

    const full = `${p.last_name} ${p.middle_name} ${p.first_name}`.trim();
    const short = abbreviateName(p);

    const base = mode === "short" ? short : full;
    return showSurName && surName ? `${surName} – ${base}` : base;
  };

  // ================================================================
  // Xóa quan hệ
  // ================================================================
  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API_BASE}/marriage/${id}`);
      setMessage("🗑️ Đã xóa quan hệ hôn nhân!");
      setDeleteConfirmId(null);
      fetchMarriages();
    } catch {
      setMessage("❌ Lỗi khi xóa bản ghi!");
    }
  };

  // ================================================================
  // UI
  // ================================================================
  return (
    <div className="bg-white p-4 rounded-xl shadow border">
      <h3 className="text-xl font-bold text-blue-600 mb-4 text-center">
        📋 Danh Sách Quan Hệ Hôn Nhân
      </h3>

      {/* Bộ lọc */}
      <div className="flex flex-wrap justify-center gap-4 mb-4">
        <div className="flex items-center gap-2">
          <span className="text-gray-700 font-medium">Kiểu hiển thị tên:</span>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            className="border p-2 rounded"
          >
            <option value="full">Đầy đủ</option>
            <option value="short">Rút gọn</option>
          </select>
        </div>

        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={showSurName}
            onChange={() => setShowSurName(!showSurName)}
            className="w-4 h-4 accent-blue-600"
          />
          <span className="font-medium text-gray-700">Tên hiệu</span>
        </label>
      </div>

      {/* Thông báo */}
      {message && (
        <p
          className={`text-center font-semibold mb-2 ${
            message.startsWith("🗑️") ? "text-green-600" : "text-red-500"
          }`}
        >
          {message}
        </p>
      )}

      {/* Bảng */}
      <div className="overflow-x-auto">
        <table className="min-w-full border text-sm text-center">
          <thead className="bg-blue-50">
            <tr>
              <th className="border p-2">#</th>
              <th className="border p-2">Người thứ nhất</th>
              <th className="border p-2">Người thứ hai</th>
              <th className="border p-2">Ngày bắt đầu</th>
              <th className="border p-2">Ngày kết thúc</th>
              <th className="border p-2">Trạng thái</th>
              <th className="border p-2">Địa điểm</th>
              <th className="border p-2">Thao tác</th>
            </tr>
          </thead>

          <tbody>
            {marriages.length === 0 ? (
              <tr>
                <td colSpan="8" className="p-4 text-gray-500">
                  Không có dữ liệu
                </td>
              </tr>
            ) : (
              marriages.map((m, idx) => (
                <tr key={m.id} className="hover:bg-gray-50">
                  <td className="border p-2">{idx + 1}</td>

                  <td className="border p-2">
                    {buildDisplayName(m.spouse_a_name, m.spouse_a_sur)}
                  </td>

                  <td className="border p-2">
                    {buildDisplayName(m.spouse_b_name, m.spouse_b_sur)}
                  </td>

                  <td className="border p-2">{formatDateVN(m.start_date)}</td>
                  <td className="border p-2">{formatDateVN(m.end_date)}</td>
                  <td className="border p-2 capitalize">{m.status}</td>
                  <td className="border p-2">{m.location}</td>

                  <td className="border p-2">
                    {deleteConfirmId === m.id ? (
                      <div className="text-red-600 font-medium">
                        Xác nhận xóa?
                        <div className="flex justify-center gap-2 mt-1">
                          <button
                            onClick={() => handleDelete(m.id)}
                            className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                          >
                            Xóa
                          </button>
                          <button
                            onClick={() => setDeleteConfirmId(null)}
                            className="bg-gray-300 px-2 py-1 rounded hover:bg-gray-400"
                          >
                            Hủy
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div className="flex justify-center gap-2">
                        <button
                          onClick={() => onEdit(m.id)}
                          className="bg-yellow-400 text-white px-2 py-1 rounded hover:bg-yellow-500"
                        >
                          ✏️
                        </button>

                        <button
                          onClick={() => setDeleteConfirmId(m.id)}
                          className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                        >
                          🗑️
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
