import React, { useState, useEffect } from "react";
import ParentDropdown from "./ParentDropdown";
// ==================================================
// ParentChildCRUD.jsx
// CV3.4 – FRONTEND UX FINAL
// - Không gọi backend
// - Logic Add/Update/Delete xử lý ở CV4
// ==================================================
function ParentChildCRUD({ persons }) {
  const [list, setList] = useState([]);
  const [form, setForm] = useState({});
  const [selectedChild, setSelectedChild] = useState(null);
  const [fatherId, setFatherId] = useState(null);
  const [motherId, setMotherId] = useState(null);
  
  async function handleAdd(e) {
    e.preventDefault();
    console.log("ADD (mock)", form);
  }

  async function handleUpdate(e) {
    e.preventDefault();
    console.log("UPDATE (mock)", form);
  }

  async function handleDelete(id) {
    console.log("DELETE (mock)", id);
  }
  
  return (
    <div className="p-6 bg-white shadow rounded mb-8">
      <h2 className="text-2xl font-bold mb-4">👨‍👩‍👧 Parent – Child</h2>

      <form
        onSubmit={form.id ? handleUpdate : handleAdd}
        className="flex flex-wrap gap-2 mb-4 items-center"
      >
        {/* 1️⃣ CHỌN CHILD */}
        <select
          value={selectedChild?.id || ""}
          onChange={(e) => {
            const child = persons.find(p => p.id === Number(e.target.value));
            setSelectedChild(child);
            setForm({ ...form, child_id: e.target.value });
            setFatherId(null);
            setMotherId(null);
          }}
          className="border p-2 rounded"
        >
          <option value="">-- Child --</option>
          {persons.map(p => (
            <option key={p.id} value={p.id}>
              {p.id} - {p.sur_name} {p.first_name}
            </option>
          ))}
        </select>

        {/* 2️⃣ CHA / MẸ (CHỈ HIỆN KHI ĐÃ CHỌN CHILD) */}
        {selectedChild && (
          <>
            <ParentDropdown
              child={selectedChild}
              people={persons}
              gender="male"
              selectedParentId={fatherId}
              onSelect={(id) => {
                setFatherId(id);
                setForm({ ...form, parent_id: id });
              }}
            />

            <ParentDropdown
              child={selectedChild}
              people={persons}
              gender="female"
              selectedParentId={motherId}
              onSelect={(id) => {
                setMotherId(id);
                setForm({ ...form, parent_id: id });
              }}
            />
          </>
        )}

        {/* 3️⃣ NÚT ADD / UPDATE */}
        <button
          type="submit"
          disabled={!selectedChild || (!fatherId && !motherId)}
          className={`px-4 py-2 rounded text-white ${!selectedChild || (!fatherId && !motherId)
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-500 hover:bg-blue-600"
            }`}
        >
          {form.id ? "Update" : "Add"}
        </button>
      </form>

      <table className="w-full border-collapse border border-gray-300 text-sm">
        <thead className="bg-gray-100">
          <tr>
            <th className="border p-2">ID</th>
            <th className="border p-2">Parent</th>
            <th className="border p-2">Child</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {list.map((r) => (
            <tr key={r.id} className="hover:bg-gray-50">
              <td className="border p-2">{r.id}</td>
              <td className="border p-2">{r.parent_id}</td>
              <td className="border p-2">{r.child_id}</td>
              <td className="border p-2 flex gap-2">
                <button onClick={() => setForm(r)} className="bg-yellow-400 text-white px-2 py-1 rounded hover:bg-yellow-500">Edit</button>
                <button onClick={() => handleDelete(r.id)} className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ParentChildCRUD;


