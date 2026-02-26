import React, { useEffect, useState } from "react";
import axios from "axios";
import { formatGender } from "../utils/format";
import { API_FASTAPI } from "../api/apiConfig";
import { API_BASE_URL } from "../api/apiConfig";

export default function PersonTable() {
  const [persons, setPersons] = useState([]);

  useEffect(() => {
    axios
      .get(`${API_FASTAPI}/person/basic`)
      .then((res) => {
        console.log("API trả về:", res.data);
        setPersons(res.data);
      })
      .catch((err) => console.error("Lỗi khi fetch dữ liệu:", err));
  }, []);

  // Hàm format ngày sinh → dd-MM-yyyy hoặc chỉ hiển thị năm
  const formatBirthDate = (dateStr) => {
    if (!dateStr) return "-";
    const d = new Date(dateStr);
    if (isNaN(d)) return "-";

    const day = d.getDate().toString().padStart(2, "0");
    const month = (d.getMonth() + 1).toString().padStart(2, "0");
    const year = d.getFullYear();

    // Nếu là 01-01-yyyy thì chỉ hiện năm
    if (day === "01" && month === "01") {
      return year.toString();
    }

    return `${day}-${month}-${year}`;
  };

  // Hàm lấy năm sinh
  const getYear = (dateStr) => {
    if (!dateStr) return "-";
    const d = new Date(dateStr);
    if (isNaN(d)) return "-";
    return d.getFullYear();
  };

  // Sort: năm sinh ↑, nếu trùng thì sort theo tên chính (ABC)
  const sortedPersons = [...persons].sort((a, b) => {
    const yearA = getYear(a.birth_date);
    const yearB = getYear(b.birth_date);

    if (yearA === "-" && yearB !== "-") return 1;
    if (yearB === "-" && yearA !== "-") return -1;

    if (yearA !== yearB) return yearA - yearB;
    return (a.first_name || "").localeCompare(b.first_name || "");
  });

  const handleEdit = (person) => {
    alert(`✏️ Sửa thành viên ID ${person.person_id} (sẽ phát triển sau).`);
    console.log("Edit:", person);
  };

  const handleDelete = (id) => {
    if (window.confirm("Bạn có chắc muốn xóa thành viên này?")) {
      alert(`🗑️ Đã xóa ID ${id} (chức năng thật sẽ phát triển sau).`);
      console.log("Delete:", id);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">📋 Bảng thành viên</h2>

      <div className="overflow-x-auto">
        <table className="table-auto border-collapse border border-gray-400 w-full">
          <thead>
            <tr className="bg-gray-200">
              <th className="border border-gray-400 px-2 py-1">ID</th>
              <th className="border border-gray-400 px-2 py-1">Tên hiệu</th>
              <th className="border border-gray-400 px-2 py-1">Tên họ</th>
              <th className="border border-gray-400 px-2 py-1">Tên đệm</th>
              <th className="border border-gray-400 px-2 py-1">Tên chính</th>
              <th className="border border-gray-400 px-2 py-1">Giới tính</th>
              <th className="border border-gray-400 px-2 py-1">Ngày sinh</th>
              <th className="border border-gray-400 px-2 py-1">Năm sinh</th>
              <th className="border border-gray-400 px-2 py-1">Hành động</th>
            </tr>
          </thead>
          <tbody>
            {sortedPersons.length > 0 ? (
              sortedPersons.map((p) => {
                const year = getYear(p.birth_date);
                return (
                  <tr key={p.person_id} className="hover:bg-gray-100">
                    <td className="border border-gray-400 px-2 py-1 text-center">
                      {p.person_id}
                    </td>
                    <td className="border border-gray-400 px-2 py-1">
                      {p.sur_name || p.sur_name || "-"}
                    </td>
                    <td className="border border-gray-400 px-2 py-1">
                      {p.last_name || "-"}
                    </td>
                    <td className="border border-gray-400 px-2 py-1">
                      {p.middle_name || "-"}
                    </td>
                    <td className="border border-gray-400 px-2 py-1">
                      {p.first_name || "-"}
                    </td>
                    <td className="border border-gray-400 px-2 py-1 text-center">
                      {formatGender(p.gender)}
                    </td>
                    <td className="border border-gray-400 px-2 py-1 text-right">
                      {formatBirthDate(p.birth_date)}
                    </td>
                    <td className="border border-gray-400 px-2 py-1 text-center">
                      {year}
                    </td>
                    <td className="border border-gray-400 px-2 py-1 text-center">
                      <button
                        onClick={() => handleEdit(p)}
                        className="bg-yellow-400 text-black px-2 py-1 rounded hover:bg-yellow-500 mr-2"
                      >
                        ✏️ Sửa
                      </button>
                      <button
                        onClick={() => handleDelete(p.person_id)}
                        className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                      >
                        🗑️ Xóa
                      </button>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td
                  colSpan="9"
                  className="border border-gray-400 text-center py-2"
                >
                  Không có dữ liệu
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
