import React from "react";
import PersonBasicForm from "./components/person/PersonBasicForm";

function PersonBasicPage({ role }) {
  return (
    <div className="max-w-2xl mx-auto bg-white shadow rounded p-6">
      <h1 className="text-2xl font-bold text-indigo-600 mb-4">
        Quản Lý Thành Viên
      </h1>

      {role === "viewer" ? (
        <p className="text-red-500 text-center">
          ❌ Bạn không có quyền truy cập trang này.
        </p>
      ) : (
        <PersonBasicForm role={role} mode="create" />
      )}
    </div>
  );
}

export default PersonBasicPage;
