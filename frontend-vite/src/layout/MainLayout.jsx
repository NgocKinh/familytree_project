import React from "react";
import Navbar from "../components/Navbar";

function MainLayout({ children }) {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Navbar */}
      <Navbar />

      {/* Nội dung trang */}
      <main className="flex-grow p-4 bg-gray-50">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white text-center p-3">
        © 2025 Family Tree Project
      </footer>
    </div>
  );
}

export default MainLayout;
