import React from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ element: Component, role, allowedRoles }) => {
  if (!allowedRoles.includes(role)) {
    return <Navigate to="/tree" replace />; // redirect về Cây Gia Phả
  }
  return <Component role={role} />;
};

export default ProtectedRoute;
