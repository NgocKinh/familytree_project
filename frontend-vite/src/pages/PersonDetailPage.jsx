import React from "react";
import PersonDetailForm from "../components/person/PersonDetailForm";

function PersonDetailPage({ role, mode = "create", personId = null }) {
  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-center mb-6 text-blue-700">
        Quản Lý Thành Viên (Chi Tiết)
      </h1>

      <PersonDetailForm role={role} mode={mode} personId={personId} />
    </div>
  );
}

export default PersonDetailPage;
