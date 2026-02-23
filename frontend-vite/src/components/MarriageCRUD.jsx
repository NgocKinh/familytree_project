import React, { useState, useEffect } from "react";
import { getAllMarriages, createMarriage, updateMarriage, deleteMarriage } from "../api/marriageApi";

function MarriageCRUD({ persons }) {
  const [list, setList] = useState([]);
  const [form, setForm] = useState({});

  useEffect(() => { loadData(); }, []);

  async function loadData() {
    const res = await getAllMarriages();
    setList(res.data);
  }

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleAdd(e) {
    e.preventDefault();
    await createMarriage(form);
    setForm({});
    loadData();
  }

  async function handleUpdate(e) {
    e.preventDefault();
    if (!form.id) return;
    await updateMarriage(form.id, form);
    setForm({});
    loadData();
  }

  async function handleDelete(id) {
    await deleteMarriage(id);
    loadData();
  }

  return (
    <div className="p-6 bg-white shadow rounded mb-8">
      <h2 className="text-2xl font-bold mb-4">💍 Marriage</h2>

      <form onSubmit={form.id ? handleUpdate : handleAdd} className="flex flex-wrap gap-2 mb-4">
        <select name="spouse_a_id" value={form.spouse_a_id || ""} onChange={handleChange} className="border p-2 rounded">
          <option value="">-- Spouse A --</option>
          {persons.map((p) => <option key={p.id} value={p.id}>{p.id} - {p.sur_name} {p.first_name}</option>)}
        </select>
        <select name="spouse_b_id" value={form.spouse_b_id || ""} onChange={handleChange} className="border p-2 rounded">
          <option value="">-- Spouse B --</option>
          {persons.map((p) => <option key={p.id} value={p.id}>{p.id} - {p.sur_name} {p.first_name}</option>)}
        </select>
        <input name="start_date" placeholder="Start YYYY-MM-DD" value={form.start_date || ""} onChange={handleChange} className="border p-2 rounded" />
        <input name="end_date" placeholder="End YYYY-MM-DD" value={form.end_date || ""} onChange={handleChange} className="border p-2 rounded" />
        <select name="status" value={form.status || ""} onChange={handleChange} className="border p-2 rounded">
          <option value="married">Married</option>
          <option value="separated">Separated</option>
          <option value="divorced">Divorced</option>
          <option value="widowed">Widowed</option>
        </select>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">{form.id ? "Update" : "Add"}</button>
      </form>

      <table className="w-full border-collapse border border-gray-300 text-sm">
        <thead className="bg-gray-100">
          <tr>
            <th className="border p-2">ID</th>
            <th className="border p-2">Spouse A</th>
            <th className="border p-2">Spouse B</th>
            <th className="border p-2">Start</th>
            <th className="border p-2">End</th>
            <th className="border p-2">Status</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {list.map((m) => (
            <tr key={m.id} className="hover:bg-gray-50">
              <td className="border p-2">{m.id}</td>
              <td className="border p-2">{m.spouse_a_id}</td>
              <td className="border p-2">{m.spouse_b_id}</td>
              <td className="border p-2">{m.start_date}</td>
              <td className="border p-2">{m.end_date || "-"}</td>
              <td className="border p-2">{m.status}</td>
              <td className="border p-2 flex gap-2">
                <button onClick={() => setForm(m)} className="bg-yellow-400 text-white px-2 py-1 rounded hover:bg-yellow-500">Edit</button>
                <button onClick={() => handleDelete(m.id)} className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default MarriageCRUD;

