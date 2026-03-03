import React, { useEffect, useState } from "react";
import { getPersonBasicList } from "../../api/personBasicApi";
import {
  addParentChild,
  getParentChildList,
  getParentChildById,
  updateParentChild,
} from "../../api/parentChildApi";

/**
 * 🔹 ParentChildForm FINAL v10
 * - Giữ nguyên logic validation cũ
 * - ✅ Load dữ liệu cũ khi sửa
 * - ✅ Hiển thị năm sinh sau tên
 */

export default function ParentChildForm({ role = "admin", editId = null, onBack }) {
  if (role === "viewer") {
    return (
      <p className="text-red-500 text-center">
        ❌ Bạn không có quyền thêm quan hệ cha – con.
      </p>
    );
  }

  const [persons, setPersons] = useState([]);
  const [relations, setRelations] = useState([]);
  const [formData, setFormData] = useState({
    parent_id: "",
    child_id: "",
    type: "",
    notes: "",
  });
  const [showSurName, setShowSurName] = useState(true);
  const [mode, setMode] = useState("full");
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  // ===============================
  // 🔹 Load danh sách thành viên và quan hệ
  // ===============================
  useEffect(() => {
    async function fetchData() {
      try {
        const personData = await getPersonBasicList();
        console.log("📌 DEBUG ParentChild persons:", personData);
        setPersons(personData.filter(p => Number(p.delete_status) === 0));

      } catch (err) {
        console.error("❌ Lỗi tải danh sách person:", err);
        setErrorMsg("Không thể tải danh sách thành viên!");
      }

      try {
        const relationData = await getParentChildList();
        setRelations(relationData);
      } catch (err) {
        console.error("❌ Lỗi tải danh sách quan hệ:", err);
      }
    }
    fetchData();
  }, []);

  // ===============================
  // 🔹 Load dữ liệu cũ khi sửa
  // ===============================
  useEffect(() => {
    if (editId) loadOldData(editId);
  }, [editId]);

  const loadOldData = async (id) => {
    try {
      const data = await getParentChildById(id);
      if (data) {
        setFormData({
          parent_id: data.parent_id || "",
          child_id: data.child_id || "",
          type: data.type || "",
          notes: data.notes || "",
        });
      }
    } catch (err) {
      console.error("❌ Lỗi load dữ liệu cũ:", err);
      setErrorMsg("Không thể tải dữ liệu quan hệ cần chỉnh sửa!");
    }
  };

  // ===============================
  // 🔹 Cập nhật form
  // ===============================
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrorMsg("");
    setSuccessMsg("");
  };

  const resetForm = () => {
    setFormData({ parent_id: "", child_id: "", type: "", notes: "" });
    setErrorMsg("");
    setSuccessMsg("");
  };

  // ===============================
  // 🔹 Validation
  // ===============================
  const validateRelation = (parent_id, child_id) => {
    if (!parent_id || !child_id)
      return "⚠️ Vui lòng chọn đầy đủ Cha/Mẹ và Con.";
    if (parent_id === child_id)
      return "❌ Cha/Mẹ và Con không thể là cùng một người!";

    const reverse = relations.find(
      (r) => r.parent_id === child_id && r.child_id === parent_id
    );
    if (reverse)
      return "❌ Quan hệ ngược chiều! Con đã là cha/mẹ của người kia.";

    const isDescendant = (currentId, targetId, depth = 0) => {
      if (depth > 20) return false;
      const children = relations
        .filter((r) => r.parent_id === currentId)
        .map((r) => r.child_id);
      if (children.includes(targetId)) return true;
      for (const c of children) {
        if (isDescendant(c, targetId, depth + 1)) return true;
      }
      return false;
    };
    if (isDescendant(child_id, parent_id))
      return "❌ Quan hệ không hợp lệ (tạo vòng lặp nhiều đời).";

    return "";
  };

  // ===============================
  // 🔹 Submit form
  // ===============================
  const handleSubmit = async (e) => {
    e.preventDefault();
    const { parent_id, child_id, type, notes } = formData;

    const validationError = validateRelation(Number(parent_id), Number(child_id));
    if (validationError) {
      setErrorMsg(validationError);
      setSuccessMsg("");
      return;
    }

    if (!type) {
      setErrorMsg("⚠️ Vui lòng chọn loại quan hệ (Cha hoặc Mẹ).");
      return;
    }

    try {
      let res;
      if (editId) {
        // ✅ Cập nhật nếu đang sửa
        res = await updateParentChild(editId, { parent_id, child_id, type, notes });
      } else {
        // ✅ Thêm mới
        res = await addParentChild({ parent_id, child_id, type, notes });
        resetForm();
      }

      setSuccessMsg(res.message || "✅ Lưu quan hệ thành công!");
      setErrorMsg("");

      const updated = await getParentChildList();
      setRelations(updated);

      if (editId && onBack) onBack(); // quay lại danh sách sau khi sửa
    } catch (err) {
      console.error("❌ Lỗi khi lưu quan hệ:", err);
      setErrorMsg("❌ Không thể lưu quan hệ (kiểm tra backend).");
      setSuccessMsg("");
    }
  };

  // ===============================
  // 🔹 Rút gọn & hiển thị tên
  // ===============================
  const abbreviateName = (p) => {
    const initials = [p.last_name, p.middle_name]
      .filter(Boolean)
      .map((part) => part.trim()[0].toUpperCase() + ".")
      .join(" ");
    const namePart = p.first_name ? p.first_name.trim() : "";
    return `${initials} ${namePart}`.trim();
  };

  const buildFullName = (p) => {
    const fullName = [p.last_name, p.middle_name, p.first_name]
      .filter(Boolean)
      .join(" ")
      .trim();

    const shortName = abbreviateName(p);
    const baseName = mode === "short" ? shortName : fullName;

    if (showSurName && p.sur_name) {
      return `${p.sur_name} – ${baseName}`;
    }
    return baseName;
  };

  const renderOptions = () =>
    persons.map((p) => {
      const birthYear = p.birth_date ? new Date(p.birth_date).getFullYear() : "";
      const displayName = `${buildFullName(p)}${birthYear ? ` (${birthYear})` : ""}`;
      return (
        <option key={p.person_id} value={p.person_id}>
          {p.person_id} – {displayName}
        </option>
      );
    });

  // ===============================
  // 🔹 UI
  // ===============================
  return (
    <div className="max-w-3xl mx-auto p-6 bg-white shadow-lg rounded-xl mt-6">
      <h2 className="text-2xl font-bold text-blue-700 mb-4 text-center">
        {editId ? "✏️ Chỉnh Sửa Quan Hệ Cha/Mẹ – Con" : "👨‍👩‍👧‍👦 Thêm Quan Hệ Cha/Mẹ – Con"}
      </h2>

      {/* 🎛️ Điều khiển hiển thị */}
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

      {/* 🧾 Form nhập liệu */}
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Parent */}
        <div>
          <label className="block mb-1 font-medium text-gray-700">👨‍👩 Chọn Cha hoặc Mẹ:</label>
          <select
            name="parent_id"
            value={formData.parent_id}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded p-2"
          >
            <option value="">-- Chọn người --</option>
            {renderOptions()}
          </select>
        </div>

        {/* Child */}
        <div>
          <label className="block mb-1 font-medium text-gray-700">🧒 Chọn Con:</label>
          <select
            name="child_id"
            value={formData.child_id}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded p-2"
          >
            <option value="">-- Chọn người --</option>
            {renderOptions()}
          </select>
        </div>

        {/* Type */}
        <div>
          <label className="block mb-1 font-medium text-gray-700">⚖️ Loại Quan Hệ:</label>
          <select
            name="type"
            value={formData.type}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded p-2"
          >
            <option value="">-- Chọn loại --</option>
            <option value="FATHER">Cha</option>
            <option value="MOTHER">Mẹ</option>
          </select>
        </div>

        {/* Notes */}
        <div>
          <label className="block mb-1 font-medium text-gray-700">📝 Ghi chú:</label>
          <input
            type="text"
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            placeholder="Ví dụ: Cha ruột, Mẹ nuôi..."
            className="w-full border border-gray-300 rounded p-2"
          />
        </div>

        {/* Thông báo */}
        {errorMsg && (
          <div className="mt-3 p-2 bg-red-100 text-red-700 rounded text-center font-medium">
            {errorMsg}
          </div>
        )}
        {successMsg && (
          <div className="mt-3 p-2 bg-green-100 text-green-700 rounded text-center font-medium">
            {successMsg}
          </div>
        )}

        {/* Nút hành động */}
        <div className="flex justify-between gap-4 pt-2">
          <button
            type="submit"
            className="flex-1 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            💾 Lưu Quan Hệ
          </button>
          <button
            type="button"
            onClick={onBack || resetForm}
            className="flex-1 bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
          >
            ⬅️ {editId ? "Quay lại" : "Hủy / Nhập lại"}
          </button>
        </div>
      </form>
    </div>
  );
}
