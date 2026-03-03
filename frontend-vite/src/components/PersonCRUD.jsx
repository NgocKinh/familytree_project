import React, { useState, useEffect } from "react";
import { getAllPersons, createPerson, updatePerson, deletePerson } from "../api/personApi";

function PersonCRUD() {
  const [persons, setPersons] = useState([]);
  const [form, setForm] = useState({});

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    const res = await getAllPersons();
    setPersons(res.data);
  }

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleAdd(e) {
    e.preventDefault();
    await createPerson(form);
    setForm({});
    loadData();
  }

  async function handleUpdate(e) {
    e.preventDefault();
    if (!form.id) return;
    await updatePerson(form.id, form);
    setForm({});
    loadData();
  }

  async function handleDelete(id) {
    await deletePerson(id);
    loadData();
  }

  return (
    <div className="p-6 bg-white shadow rounded mb-8">
      <h2 className="text-2xl font-bold mb-4">👤 Person</h2>

      <form onSubmit={form.id ? handleUpdate : handleAdd} className="flex flex-wrap gap-2 mb-4">
        <input name="sur_name" placeholder="Sure Name" value={form.sur_name || ""} onChange={handleChange} className="border p-2 rounded flex-1" />
        <input name="last_name" placeholder="Last Name" value={form.last_name || ""} onChange={handleChange} className="border p-2 rounded flex-1" />
        <input name="middle_name" placeholder="Middle Name" value={form.middle_name || ""} onChange={handleChange} className="border p-2 rounded flex-1" />
        <input name="first_name" placeholder="First Name" value={form.first_name || ""} onChange={handleChange} className="border p-2 rounded flex-1" />
        <select name="gender" value={form.gender || ""} onChange={handleChange} className="border p-2 rounded">
          <option value="unknown">Unknown</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
        <input name="birth_date" placeholder="Birth YYYY-MM-DD" value={form.birth_date || ""} onChange={handleChange} className="border p-2 rounded" />
        <input name="death_date" placeholder="Death YYYY-MM-DD" value={form.death_date || ""} onChange={handleChange} className="border p-2 rounded" />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">{form.id ? "Update" : "Add"}</button>
      </form>

      <table className="w-full border-collapse border border-gray-300 text-sm">
        <thead className="bg-gray-100">
          <tr>
            <th className="border p-2">ID</th>
            <th className="border p-2">Name</th>
            <th className="border p-2">Birth</th>
            <th className="border p-2">Death</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {persons.map((p) => (
            <tr key={p.id} className="hover:bg-gray-50">
              <td className="border p-2">{p.id}</td>
              <td className="border p-2">{`${p.sur_name || ""} ${p.middle_name || ""} ${p.first_name || ""}`}</td>
              <td className="border p-2">{p.birth_date}</td>
              <td className="border p-2">{p.death_date || "-"}</td>
              <td className="border p-2 flex gap-2">
                <button onClick={() => setForm(p)} className="bg-yellow-400 text-white px-2 py-1 rounded hover:bg-yellow-500">Edit</button>
                <button onClick={() => handleDelete(p.id)} className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PersonCRUD;
