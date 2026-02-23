import React from "react";
import PersonList from "../pages/PersonList";

function PersonPage({ role }) {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Danh Sách Thành Viên</h1>
      <PersonList role={role} />
    </div>
  );
}

export default PersonPage;

