import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { addPerson, updatePerson, getPersonById } from "../api/personApi";

function PersonForm({ role = "viewer" }) {
  const { id } = useParams();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    sur_name: "",
    last_name: "",
    middle_name: "",
    first_name: "",
    gender: "",
    birth_date: "",
    birth_date_precision: "unknown",
    death_date: "",
    death_date_precision: "unknown",
    asian_birth_date: "",
    asian_birth_precision: "unknown",
    asian_death_date: "",
    asian_death_precision: "unknown",
    birth_place: "",
    death_place: "",
    grave_info: "",
    nationality: "",
    ethnic_group: "",
    religion: "",
    languages_spoken: "",
    address: "",
    phone_number: "",
    school_attended: "",
    degree_earned: "",
    notes: "",
    avatar: null,
    lineage_id: "", // chỉ hiện cho cooperator/admin
  });

  // Nếu có id thì load dữ liệu
  useEffect(() => {
    if (id && role !== "viewer") {
      getPersonById(id).then((data) => setFormData(data));
    }
  }, [id, role]);

  // Không cho viewer vào
  if (role === "viewer") {
    return <p className="text-center text-red-500">Bạn không có quyền truy cập form này.</p>;
  }

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    if (type === "file") {
      setFormData((prev) => ({ ...prev, [name]: files[0] }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (id) {
        await updatePerson(id, formData);
        alert("Cập nhật thành công!");
      } else {
        await addPerson(formData);
        alert("Thêm thành công!");
      }
      navigate("/list");
    } catch (err) {
      console.error(err);
      alert("Lỗi khi lưu!");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 space-y-4 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-center">
        {id ? "Sửa thành viên" : "Thêm thành viên mới"}
      </h2>

      {/* Avatar */}
      <div>
        <label className="block font-medium">Ảnh đại diện</label>
        <input type="file" name="avatar" onChange={handleChange} />
      </div>

      {/* Các field cơ bản cho Member */}
      <div>
        <label className="block">Họ (sur_name)</label>
        <input
          type="text"
          name="sur_name"
          value={formData.sur_name || ""}
          onChange={handleChange}
          className="w-full border px-2 py-1 rounded"
        />
      </div>

      <div>
        <label className="block">Tên (first_name)</label>
        <input
          type="text"
          name="first_name"
          value={formData.first_name || ""}
          onChange={handleChange}
          className="w-full border px-2 py-1 rounded"
        />
      </div>

      <div>
        <label className="block">Giới tính</label>
        <select
          name="gender"
          value={formData.gender || ""}
          onChange={handleChange}
          className="w-full border px-2 py-1 rounded"
        >
          <option value="male">Nam</option>
          <option value="female">Nữ</option>
          <option value="other">Khác</option>
          <option value="unknown">Không rõ</option>
        </select>
      </div>

      {/* Quốc tịch & dân tộc - dropdown */}
      <div>
        <label className="block">Quốc tịch</label>
        <select
          name="nationality"
          value={formData.nationality || ""}
          onChange={handleChange}
          className="w-full border px-2 py-1 rounded"
        >
          <option value="">-- Chọn quốc tịch --</option>
          <option value="Vietnamese">Việt Nam</option>
          <option value="American">Mỹ</option>
          <option value="French">Pháp</option>
        </select>
      </div>

      <div>
        <label className="block">Dân tộc</label>
        <select
          name="ethnic_group"
          value={formData.ethnic_group || ""}
          onChange={handleChange}
          className="w-full border px-2 py-1 rounded"
        >
          <option value="">-- Chọn dân tộc --</option>
          <option value="Kinh">Kinh</option>
          <option value="Tày">Tày</option>
          <option value="Nùng">Nùng</option>
          <option value="Khmer">Khmer</option>
        </select>
      </div>

      {/* Chỉ cho Cooperator/Admin nhập lineage_id */}
      {(role === "cooperator" || role === "admin") && (
        <div>
          <label className="block">Dòng họ (lineage_id)</label>
          <input
            type="number"
            name="lineage_id"
            value={formData.lineage_id || ""}
            onChange={handleChange}
            className="w-full border px-2 py-1 rounded"
          />
        </div>
      )}

      {/* Notes */}
      <div>
        <label className="block">Ghi chú</label>
        <textarea
          name="notes"
          value={formData.notes || ""}
          onChange={handleChange}
          className="w-full border px-2 py-1 rounded"
        />
      </div>

      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {id ? "Cập nhật" : "Thêm mới"}
      </button>
    </form>
  );
}

export default PersonForm;

