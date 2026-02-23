import React, { useState, useEffect } from "react";
import { addPerson, updatePerson } from "../api/personApi";
import maleAvatar from "../assets/male.png";
import femaleAvatar from "../assets/female.png";
import otherAvatar from "../assets/other.png";

const PersonForm = ({ initialData = {}, onSubmit, role = "viewer", mode = "add" }) => {
  const [formData, setFormData] = useState({
    sur_name: "",
    last_name: "",
    middle_name: "",
    first_name: "",
    gender: "male",
    birth_date: "",
    death_date: "",
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
    avatar: "",
  });

  useEffect(() => {
    if (initialData) {
      setFormData((prev) => ({ ...prev, ...initialData }));
    }
  }, [initialData]);

  if (role === "viewer") {
    return <p className="text-red-500 text-center">🚫 Bạn không có quyền truy cập form này.</p>;
  }

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    if (type === "file") {
      setFormData((prev) => ({ ...prev, avatar: URL.createObjectURL(files[0]) }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (mode === "edit") {
        await updatePerson(formData.person_id, formData);
      } else {
        await addPerson(formData);
      }
      if (onSubmit) onSubmit(formData);
    } catch (err) {
      console.error("Error submitting form", err);
    }
  };

  const getDefaultAvatar = () => {
    if (formData.avatar) return formData.avatar;
    if (formData.gender === "male") return maleAvatar;
    if (formData.gender === "female") return femaleAvatar;
    return otherAvatar;
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-5xl mx-auto bg-white p-6 border rounded shadow"
    >
      <h2 className="text-2xl font-bold text-center mb-6">
        {mode === "edit" ? "Sửa thông tin thành viên" : "Thêm thành viên mới"}
      </h2>

      <div className="grid grid-cols-3 gap-6">
        {/* Cột avatar */}
        <div className="col-span-1 flex flex-col items-center space-y-3">
          <img
            src={getDefaultAvatar()}
            alt="avatar"
            className="w-32 h-32 object-cover rounded-full border"
          />
          <input type="file" name="avatar" onChange={handleChange} />
          <input
            type="text"
            placeholder="Link URL ảnh"
            onChange={(e) => setFormData((p) => ({ ...p, avatar: e.target.value }))}
            className="w-full border p-1 rounded"
          />
        </div>

        {/* Cột form bên phải */}
        <div className="col-span-2 grid grid-cols-2 gap-4">
          {[
            { label: "Tên hiệu", name: "sur_name" },
            { label: "Tên họ", name: "last_name" },
            { label: "Tên đệm", name: "middle_name" },
            { label: "Tên chính", name: "first_name" },
            { label: "Ngày sinh", name: "birth_date", type: "date" },
            { label: "Ngày mất", name: "death_date", type: "date" },
            { label: "Nơi sinh", name: "birth_place" },
            { label: "Nơi mất", name: "death_place" },
            { label: "Thông tin mộ", name: "grave_info" },
            { label: "Quốc tịch", name: "nationality" },
            { label: "Dân tộc", name: "ethnic_group" },
            { label: "Tôn giáo", name: "religion" },
            { label: "Ngôn ngữ", name: "languages_spoken" },
            { label: "Điện thoại/Email", name: "phone_number" },
            { label: "Địa chỉ", name: "address" },
            { label: "Trường học", name: "school_attended" },
            { label: "Bằng cấp", name: "degree_earned" },
          ].map((field) => (
            <div key={field.name}>
              <label className="block font-medium">{field.label}</label>
              <input
                type={field.type || "text"}
                name={field.name}
                value={formData[field.name] || ""}
                onChange={handleChange}
                className="w-full border p-1 rounded"
              />
            </div>
          ))}

          {/* Gender riêng vì là select */}
          <div>
            <label className="block font-medium">Giới tính</label>
            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              className="w-full border p-1 rounded"
            >
              <option value="male">Nam</option>
              <option value="female">Nữ</option>
              <option value="other">Khác</option>
            </select>
          </div>
        </div>
      </div>

      {/* Notes */}
      <div className="mt-4">
        <label className="block font-medium">Ghi chú</label>
        <textarea
          name="notes"
          value={formData.notes}
          onChange={handleChange}
          className="w-full border p-2 rounded"
        />
      </div>

      {/* Buttons */}
      <div className="flex justify-center space-x-4 mt-6">
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          {mode === "edit" ? "Cập nhật" : "Thêm mới"}
        </button>
        <button type="reset" className="bg-gray-400 text-white px-4 py-2 rounded">
          Hủy
        </button>
      </div>
    </form>
  );
};

export default PersonForm;
