// ======================================================================
// File: src/components/person/PersonBasicForm.jsx
// ======================================================================

import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import {
  addPerson,
  updatePerson,
  getPersonById,
  checkDuplicatePerson,
  uploadAvatar,
} from "../../api/personApi";

import maleAvatar from "../../assets/male.png";
import femaleAvatar from "../../assets/female.png";
import otherAvatar from "../../assets/other.png";

import {
  formatDateVN,
  parseVNDate,
  detectPrecision,
} from "../../utils/formatDate";

export default function PersonBasicForm({ role, onSaved }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(id && id !== "new");

  // =========================
  // STATE
  // =========================
  const [form, setForm] = useState({
    sur_name: "",
    last_name: "",
    middle_name: "",
    first_name: "",
    gender: "",
    birth_date: "",
    death_date: "",
    birth_date_precision: "unknown",
    death_date_precision: "unknown",
  });

  const [avatarPreview, setAvatarPreview] = useState(null);
  const [showPendingModal, setShowPendingModal] = useState(false);
  const [duplicateMessage, setDuplicateMessage] = useState("");

  // =========================
  // RESET FORM
  // =========================
  const resetForm = () => {
    setForm({
      sur_name: "",
      last_name: "",
      middle_name: "",
      first_name: "",
      gender: "",
      birth_date: "",
      death_date: "",
      birth_date_precision: "unknown",
      death_date_precision: "unknown",
    });
    setAvatarPreview(null);
    setDuplicateMessage("");
  };

  // =========================
  // LOAD DATA (EDIT)
  // =========================
  useEffect(() => {
    if (isEdit) loadData();
  }, [id]);

  const loadData = async () => {
    try {
      const data = await getPersonById(id);
      setForm({
        sur_name: data.sur_name || "",
        last_name: data.last_name || "",
        middle_name: data.middle_name || "",
        first_name: data.first_name || "",
        gender: data.gender || "",
        birth_date: formatDateVN(
          data.birth_date,
          data.birth_date_precision
        ),
        death_date: formatDateVN(
          data.death_date,
          data.death_date_precision
        ),
        birth_date_precision: data.birth_date_precision || "unknown",
        death_date_precision: data.death_date_precision || "unknown",
      });
    } catch (err) {
      console.error("❌ Load error:", err);
    }
  };

  // =========================
  // AVATAR
  // =========================
  const fallbackGender = (gender) => {
    if (gender === "male") return maleAvatar;
    if (gender === "female") return femaleAvatar;
    return otherAvatar;
  };

  const displayAvatar =
    avatarPreview || fallbackGender(form.gender);

  // =========================
  // HANDLE CHANGE
  // =========================
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  // =========================
  // SUBMIT
  // =========================
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isEdit) {
      const dupRes = await checkDuplicatePerson({
        last_name: form.last_name,
        first_name: form.first_name,
        gender: form.gender,
      });

      if (dupRes.duplicate) {
        setDuplicateMessage(dupRes.message);
        setShowPendingModal(true);
        return;
      }
    }

    const payload = {
      ...form,
      birth_date: parseVNDate(form.birth_date),
      death_date: parseVNDate(form.death_date),
      birth_date_precision: detectPrecision(form.birth_date),
      death_date_precision: detectPrecision(form.death_date),
      role,
    };

    try {
      if (isEdit) {
        await updatePerson(id, payload);
        alert("✅ Cập nhật thành công!");
      } else {
        await addPerson(payload);
        alert("✅ Thêm thành công!");
        resetForm();
      }

      if (onSaved) onSaved();
    } catch (err) {
      console.error("❌ Submit error:", err);
      alert("Không thể lưu dữ liệu!");
    }
  };

  // =========================
  // SEND TO PENDING
  // =========================
  const sendToPending = async () => {
    try {
      await addPerson({ ...form, role });
      alert("🟡 Đã gửi Pending!");
      setShowPendingModal(false);
      resetForm();
      navigate("/pending");
    } catch (err) {
      console.error(err);
      alert("Không gửi được Pending!");
    }
  };

  // =========================
  // UI
  // =========================
  return (
    <div className="max-w-xl mx-auto p-4 border rounded shadow">
      <h2 className="text-2xl font-bold mb-4">
        {isEdit ? "Chỉnh sửa thành viên" : "Thêm thành viên mới"}
      </h2>

      {/* AVATAR */}
      <div className="flex justify-center mb-6">
        <img
          src={displayAvatar}
          alt="avatar"
          className="w-[96px] h-[128px] rounded border object-cover"
        />
      </div>

      {/* FORM */}
      <form onSubmit={handleSubmit}>
        {[
          ["👑 Tên hiệu", "sur_name"],
          ["🏡 Tên họ", "last_name"],
          ["🧩 Tên đệm", "middle_name"],
          ["🌟 Tên chính", "first_name"],
        ].map(([label, name]) => (
          <div className="mb-2" key={name}>
            <label>{label}:</label>
            <input
              name={name}
              value={form[name]}
              onChange={handleChange}
              className="border p-2 w-full"
              required={name === "last_name" || name === "first_name"}
            />
          </div>
        ))}

        <div className="mb-2">
          <label>🚻 Giới tính:</label>
          <select
            name="gender"
            value={form.gender}
            onChange={handleChange}
            className="border p-2 w-full"
            required
          >
            <option value="">-- chọn --</option>
            <option value="male">Nam</option>
            <option value="female">Nữ</option>
            <option value="other">Khác</option>
          </select>
        </div>

        <div className="mb-2">
          <label>🎂 Ngày sinh:</label>
          <input
            type="text"
            name="birth_date"
            value={form.birth_date}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>

        <div className="mb-2">
          <label>🕯 Ngày mất:</label>
          <input
            type="text"
            name="death_date"
            value={form.death_date}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>

        <div className="mt-3 flex gap-3">
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          >
            💾 Lưu
          </button>

          {!isEdit && (
            <button
              type="button"
              onClick={resetForm}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
            >
              ➕ Thêm mới
            </button>
          )}
        </div>
      </form>

      {/* MODAL PENDING */}
      {showPendingModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
          <div className="bg-white p-6 rounded shadow w-[400px]">
            <h3 className="text-xl font-bold mb-2 text-red-600">
              ⚠️ Trùng thành viên
            </h3>
            <p className="mb-3">{duplicateMessage}</p>

            <div className="text-right space-x-2">
              <button
                onClick={() => setShowPendingModal(false)}
                className="px-3 py-1 bg-gray-300 rounded"
              >
                Hủy
              </button>

              <button
                onClick={sendToPending}
                className="px-3 py-1 bg-yellow-600 text-white rounded"
              >
                🟡 Gửi Pending
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
