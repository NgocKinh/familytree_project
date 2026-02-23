import React, { useEffect, useState } from "react";
import { getParentChildList, deleteParentChild } from "../api/parentChildApi";

// Hàm rút gọn hiển thị tên
function formatDisplayName(name, mode = "full") {
  if (!name) return "";
  name = name.trim();
  if (mode === "short") {
    const parts = name.split(" ");
    if (parts.length > 1) {
      const first = parts.pop();
      const initials = parts.map((p) => p[0].toUpperCase() + ".").join(" ");
      return `${initials} ${first}`;
    }
  }
  return name;
}

function ParentChildList({ onEdit }) {
  const [relations, setRelations] = useState([]);
  const [mode, setMode] = useState("full");
  const [showSurName, setShowSurName] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const data = await getParentChildList();
    setRelations(data);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Bạn có chắc muốn xóa mối quan hệ này không?")) {
      await deleteParentChild(id);
      loadData();
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h3 className="text-xl font-bold text-gray-700 mb-4">
        📋 Danh Sách Quan Hệ Cha – Con
      </h3>

      {/* Bộ điều khiển hiển thị */}
      <div className="mb-4 flex flex-wrap items-center justify-center gap-4">
        <div className="flex items-center space-x-2">
          <label className="font-medium text-gray-700">🎛️ Kiểu hiển thị tên:</label>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            className="border border-gray-300 rounded p-2"
          >
            <option value="full">Đầy đủ</option>
            <option value="short">Rút gọn</option>
          </select>
        </div>

        <label className="flex items-center space-x-2 cursor-pointer">
          <input
            type="checkbox"
            checked={showSurName}
            onChange={() => setShowSurName(!showSurName)}
            className="w-4 h-4 accent-blue-600"
          />
          <span className="text-gray-700 font-medium">Hiển thị "Tên hiệu"</span>
        </label>
      </div>

      {/* Bảng dữ liệu */}
      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-300">
          <thead className="bg-gray-100 text-gray-700">
            <tr>
              <th className="border px-4 py-2">#</th>
              <th className="border px-4 py-2">Cha/Mẹ</th>
              <th className="border px-4 py-2">Con</th>
              <th className="border px-4 py-2">Loại</th>
              <th className="border px-4 py-2">Ghi chú</th>
              <th className="border px-4 py-2 text-center">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            {relations.map((r, index) => (
              <tr key={r.id} className="hover:bg-gray-50">
                <td className="border px-4 py-2 text-center">{index + 1}</td>

                {/* Cột Cha/Mẹ */}
                <td className="border px-4 py-2">
                  {formatDisplayName(r.parent_name, mode)}
                </td>

                {/* Cột Con */}
                <td className="border px-4 py-2">
                  {formatDisplayName(r.child_name, mode)}
                </td>

                {/* Loại */}
                <td className="border px-4 py-2 text-center">
                  {r.relation_label}
                </td>

                {/* Ghi chú */}
                <td className="border px-4 py-2">{r.notes || ""}</td>

                {/* Nút thao tác */}
                <td className="border px-4 py-2 text-center space-x-2">
                  {/* <button
                    onClick={() => onEdit(r.id)}
                    className="bg-yellow-400 hover:bg-yellow-500 text-white px-3 py-1 rounded"
                  >
                    ✏️
                  </button> */}
                  <button
                    onClick={() => handleDelete(r.id)}
                    className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                  >
                    🗑️
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ParentChildList;


