import React, { useState, useEffect } from "react";
import { getAllLineages, createLineage, updateLineage, deleteLineage } from "../api/lineageApi";

function LineageCRUD() {
  const [list, setList] = useState([]);
  const [form, setForm] = useState({});

  useEffect(() => { loadData(); }, []);

  async function loadData() {
    const res = await getAllLineages();
    setList(res.data);
  }

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleAdd(e) {
    e.preventDefault();
    await createLineage(form);
    setForm({});
    loadData();
  }

  async function handleUpdate(e) {
    e.preventDefault();
    if (!form.id) return;
    await updateLineage(form.id, form);
    setForm({});
    loadData();
  }

  async function handleDelete(id) {
    await deleteLineage(id);
    loadData();
  }

  return (
    <div className="p-6 bg-white shadow rounded mb-8">
      <h2 className="text-2xl font-bold mb-4">🌳 Lineage</h2>

      <form onSubmit={form.id ? handleUpdate : handleAdd} className="flex gap-2 mb-4">
        <input name="name" placeholder="Lineage Name" value={form.name || ""} onChange={handleChange} className="border p-2 rounded flex-1" />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">{form.id ? "Update" : "Add"}</button>
      </form>

      <table className="w-full border-collapse border border-gray-300 text-sm">
        <thead className="bg-gray-100">
          <tr>
            <th className="border p-2">ID</th>
            <th className="border p-2">Name</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {list.map((l) => (
            <tr key={l.id} className="hover:bg-gray-50">
              <td className="border p-2">{l.id}</td>
              <td className="border p-2">{l.name}</td>
              <td className="border p-2 flex gap-2">
                <button onClick={() => setForm(l)} className="bg-yellow-400 text-white px-2 py-1 rounded hover:bg-yellow-500">Edit</button>
                <button onClick={() => handleDelete(l.id)} className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default LineageCRUD;


