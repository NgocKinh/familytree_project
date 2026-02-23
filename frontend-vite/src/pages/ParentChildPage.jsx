import { useEffect, useState } from "react";
import ParentChildList from "../components/ParentChildList";
import ParentChildForm from "../components/parent_child/ParentChildForm";
import ParentChildCRUD from "../components/ParentChildCRUD";

import { getAllPersons } from "../api/personApi";

export default function ParentChildPage() {
  // ===== TAB STATE =====
  const [activeTab, setActiveTab] = useState("list"); // list | form | crud
  const [editId, setEditId] = useState(null);

  // ===== DATA FOR CV3.4 =====
  const [persons, setPersons] = useState([]);

  useEffect(() => {
  // CV3.4 DONE
  // Backend sẽ cấp persons ở CV4
  setPersons([]);
  }, []);

  // ===== HANDLERS =====
  const handleEdit = (id) => {
    setEditId(id);
    setActiveTab("form");
  };

  const handleBack = () => {
    setEditId(null);
    setActiveTab("list");
  };

  return (
    <div className="max-w-6xl mx-auto p-4 bg-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold text-center text-blue-600 mb-4">
        👨‍👩‍👧‍👦 Quản Lý Quan Hệ Cha – Con
      </h2>

      {/* ===== TAB BUTTONS ===== */}
      <div className="flex justify-center gap-4 mb-6">
        <button
          onClick={() => handleBack()}
          className={`px-4 py-2 rounded ${
            activeTab === "list"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-700"
          }`}
        >
          📋 Danh sách
        </button>

     
      </div>

      {/* ===== OPTIONAL FORM ===== */}
      
      {/* ===== TAB CONTENT ===== */}
      {activeTab === "list" && <ParentChildList onEdit={handleEdit} />}

      {activeTab === "form" && (
        <ParentChildForm editId={editId} onBack={handleBack} />
      )}


    </div>
  );
}
