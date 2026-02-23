import React from "react";
import { Link } from "react-router-dom";

/**
 * Breadcrumb Component
 * @param {Array} items - danh sách [{ label: "Trang chủ", path: "/" }, { label: "Quản lý", path: "/admin" }, { label: "Cấu hình" }]
 */
function Breadcrumb({ items = [] }) {
  return (
    <nav className="text-sm text-gray-600 mb-4" aria-label="breadcrumb">
      <ol className="flex flex-wrap items-center space-x-1">
        {items.map((item, index) => {
          const isLast = index === items.length - 1;
          return (
            <li key={index} className="flex items-center">
              {!isLast ? (
                <>
                  <Link
                    to={item.path}
                    className="hover:underline text-blue-600"
                  >
                    {item.label}
                  </Link>
                  <span className="mx-1 text-gray-400">{">"}</span>
                </>
              ) : (
                <span className="font-semibold text-gray-800">
                  {item.label}
                </span>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

export default Breadcrumb;
