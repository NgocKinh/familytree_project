import React from "react";
import { Navigate } from "react-router-dom";

/**
 * ProtectedRouteV6
 * - Chuẩn React Router v6 (children-based)
 * - Không ép truyền props xuống component con
 * - Chỉ làm 1 việc: cho qua hoặc redirect
 */
const ProtectedRouteV6 = ({ role, allowRoles, redirectTo = "/", children }) => {
  if (!allowRoles.includes(role)) {
    return <Navigate to={redirectTo} replace />;
  }
  return <>{children}</>;
};

export default ProtectedRouteV6;

