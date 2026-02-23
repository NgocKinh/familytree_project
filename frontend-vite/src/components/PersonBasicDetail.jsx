import React, { useEffect, useState } from "react";
import { getPersonBasicById } from "../api/personBasicApi";

function PersonBasicDetail({ personId }) {
  const [person, setPerson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!personId) return;

    getPersonBasicById(personId)
      .then((data) => {
        setPerson(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching person detail:", err);
        setError("Không tìm thấy dữ liệu thành viên.");
        setLoading(false);
      });
  }, [personId]);

  if (loading) return <p className="text-gray-600">⏳ Đang tải dữ liệu...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (!person) return <p className="text-gray-600">Không có dữ liệu.</p>;

  return (
    <div className="p-4 border rounded shadow bg-white">
      <h2 className="text-xl font-bold mb-4">Thông tin cơ bản</h2>
      <ul className="space-y-2">
        <li>
          <strong>Tên hiệu:</strong> {person.sur_name || "—"}
        </li>
        <li>
          <strong>Tên họ:</strong> {person.last_name || "—"}
        </li>
        <li>
          <strong>Tên đệm:</strong> {person.middle_name || "—"}
        </li>
        <li>
          <strong>Tên chính:</strong> {person.first_name || "—"}
        </li>
        <li>
          <strong>Giới tính:</strong> {person.gender}
        </li>
        <li>
          <strong>Ngày sinh:</strong> {person.birth_date || "Không rõ"}
        </li>
        <li>
          <strong>Ngày mất:</strong> {person.death_date || "—"}
        </li>
        <li>
          <strong>Nơi sinh:</strong> {person.birth_place || "Không rõ"}
        </li>
      </ul>
    </div>
  );
}

export default PersonBasicDetail;
