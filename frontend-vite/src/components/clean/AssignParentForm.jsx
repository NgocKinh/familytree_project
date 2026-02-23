import React, { useEffect, useState } from "react";
import axios from "axios";
import PersonDropdown from "../common/PersonDropdown";

function AssignParentForm() {
  // -----------------------------
  // DATA LISTS
  // -----------------------------
  const [persons, setPersons] = useState([]);
  const [marriages, setMarriages] = useState([]);

  // 🔹 Chuẩn hóa hiển thị tên (KHÔNG sửa DB)
  const displayName = (name = "") => name.replaceAll("|", " ");
  // -----------------------------
  // FORM STATE
  // -----------------------------
  const [childId, setChildId] = useState("");
  const [noMarriage, setNoMarriage] = useState(true);
  const [marriageId, setMarriageId] = useState("");

  const [parentId, setParentId] = useState("");
  const [type, setType] = useState("");

  // -----------------------------
  // UI STATE
  // -----------------------------
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [hasFather, setHasFather] = useState(false);
  const [hasMother, setHasMother] = useState(false);
  const [lockForm, setLockForm] = useState(false);
  useEffect(() => {
    axios.get("/api/person/for-person-dropdown")
      .then(res => setPersons(res.data || []))
      .catch(() => setPersons([]));

    axios.get("/api/marriage")
      .then(res => setMarriages(res.data || []))
      .catch(() => setMarriages([]));
  }, []);

  const checkParentStatus = async (id) => {
    try {
      const res = await axios.get(`/api/child/${id}/parents-status`);
      const { has_father, has_mother } = res.data;

      setHasFather(has_father);
      setHasMother(has_mother);

      if (has_father && has_mother) {
        setError("Người này đã có đủ cha mẹ. Không thể thêm. Bấm Hủy ❌ để trở về.");
        setLockForm(true);
      } else {
        setLockForm(false);
      }
    } catch {
      setError("❌ Không kiểm tra được trạng thái cha mẹ.");
      setLockForm(true);
    }
  };

  // -----------------------------
  // SUBMIT
  // -----------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!childId) {
      setError("❌ Chưa chọn người con.");
      return;
    }

    try {
      // ===============================
      // CASE 1: KHÔNG CÓ HÔN NHÂN
      // ===============================
      if (noMarriage) {
        if (!parentId || !type) {
          setError("❌ Thiếu cha/mẹ hoặc vai trò.");
          return;
        }

        await axios.post("/api/clean/parent", {
          child_id: Number(childId),
          parent_id: Number(parentId),
          type,
          marriage_id: null
        });
      }

      // ===============================
      // CASE 2: CÓ HÔN NHÂN → AUTO CHA + MẸ
      // ===============================
      else {
        const m = marriages.find(x => String(x.id) === String(marriageId));
        if (!m) {
          setError("❌ Không tìm thấy hôn nhân.");
          return;
        }

        // CHA
        await axios.post("/api/clean/parent", {
          child_id: Number(childId),
          parent_id: m.spouse_a_id,
          type: "FATHER",
          marriage_id: m.id
        });

        // MẸ
        await axios.post("/api/clean/parent", {
          child_id: Number(childId),
          parent_id: m.spouse_b_id,
          type: "MOTHER",
          marriage_id: m.id
        });
      }

      setSuccess("✅ Đã bổ sung cha/mẹ thành công.");
      // 🔄 Reset form về trạng thái ban đầu sau khi lưu thành công
      setChildId('');
      setParentId('');
      setType('');
      setMarriageId('');
      setNoMarriage(true);
      setHasFather(false);
      setHasMother(false);
      setLockForm(false);

    } catch (err) {
      setError(err.response?.data?.error || "❌ Lỗi hệ thống.");
    }
  };

  // =========================================================
  // RENDER
  // =========================================================
  return (
    <div className="max-w-xl mx-auto p-4 bg-white shadow rounded">

      {error && <div className="text-red-600 mb-2">{error}</div>}
      {success && <div className="text-green-600 mb-2">{success}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">

        {/* ================================================= */}
        {/* 1️⃣ SELECT CON */}
        {/* ================================================= */}
        <div>
          <label className="block font-semibold">1️⃣ Người Con (bắt buộc)</label>
          <PersonDropdown
            label={null}
            value={childId}
            onChange={(id) => {
              setChildId(id);
              setError("");
              setSuccess("");
              setHasFather(false);
              setHasMother(false);
              setLockForm(false);

              if (!id) return;
              checkParentStatus(id);
            }}
            persons={persons}
            placeholder="-- chọn người con --"
          />
        </div>

        {/* ================================================= */}
        {/* 2️⃣ SELECT MARRIAGE */}
        {/* ================================================= */}
        {
          childId && (
            <div>
              <label className="block font-semibold">2️⃣ Thuộc gia đình (nếu có)</label>

              <label className="block mb-2">
                <input
                  type="checkbox"
                  checked={noMarriage}
                  disabled={lockForm}
                  onChange={() => {
                    const nextNoMarriage = !noMarriage;

                    // ❌ Có đúng 1 bên cha/mẹ mà chuyển sang "thuộc gia đình" → chặn
                    if (!nextNoMarriage && (hasFather ^ hasMother)) {
                      setError("❌ Người này chỉ có 1 bên cha/mẹ, không thể gán theo gia đình.");
                      return;
                    }

                    setNoMarriage(nextNoMarriage);

                    // 🔄 Nếu CHUYỂN SANG "thuộc gia đình" → reset Cha/Mẹ
                    if (!nextNoMarriage) {
                      setParentId("");
                      setType("");
                    }

                    // luôn reset marriage khi đổi mode
                    setMarriageId("");
                  }}


                />{" "}
                Không thuộc gia đình nào
              </label>

              {!noMarriage && (
                <select
                  className="w-full border p-2 rounded"
                  value={marriageId}
                  onChange={e => setMarriageId(e.target.value)}
                >
                  <option value="">-- chọn Cha & Mẹ --</option>
                  {marriages.map(m => (
                    <option key={m.id} value={m.id}>
                      #{m.id} – {displayName(m.spouse_a_name)} & {displayName(m.spouse_b_name)}
                    </option>
                  ))}

                </select>
              )}
            </div>
          )
        }
        {/* ================================================= */}
        {/* 3️⃣ TYPE */}
        {/* ================================================= */}
        {
          childId && noMarriage && (
            <div>
              <label className="block font-semibold">
                3️⃣ Vai trò (bắt buộc)
              </label>
              <div className="flex gap-6">
                <label>
                  <input
                    type="radio"
                    value="FATHER"
                    checked={type === "FATHER"}
                    onChange={() => {
                      setType("FATHER");
                      setParentId("");   // reset chọn Cha/Mẹ khi đổi vai trò
                    }}
                    disabled={lockForm || hasFather}
                  />

                  Cha
                </label>

                <label>
                  <input
                    type="radio"
                    value="MOTHER"
                    checked={type === "MOTHER"}
                    onChange={() => {
                      setType("MOTHER");
                      setParentId("");   // reset cho đồng bộ
                    }}
                    disabled={lockForm || hasMother}
                  />

                  Mẹ
                </label>
              </div>
            </div>
          )
        }

        {/* ================================================= */}
        {/* 4️⃣ SELECT PARENT */}
        {/* ================================================= */}
        {
          childId && noMarriage && !lockForm && (
            <div>
              <label className="block font-semibold">
                4️⃣ Cha / Mẹ (bắt buộc)
              </label>
              <PersonDropdown
                label={null}
                value={parentId}
                onChange={setParentId}
                persons={persons}
                disabled={lockForm}
                filterFn={(p) => {
                  if (type === "FATHER") return p.gender === "male";
                  if (type === "MOTHER") return p.gender === "female";
                  return false;
                }}
                placeholder="-- chọn --"
              />
            </div>
          )
        }

        {/* ================================================= */}
        {/* BUTTONS */}
        {/* ================================================= */}
        <div className="flex justify-between pt-4">
          {/* NÚT HỦY */}
          <button
            type="button"
            className="px-4 py-2 bg-gray-400 text-white rounded"
            onClick={() => {
              setChildId('');
              setParentId('');
              setType('');
              setMarriageId('');
              setNoMarriage(true);
              setError('');
              setSuccess('');
              setHasFather(false);
              setHasMother(false);
              setLockForm(false);
            }}
          >
            ❌ Hủy
          </button>

          {/* NÚT LƯU */}
          <button
            type="submit"
            disabled={lockForm}
            className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
          >
            💾 Lưu
          </button>
        </div>
      </form >
    </div >
  );
}

export default AssignParentForm;

