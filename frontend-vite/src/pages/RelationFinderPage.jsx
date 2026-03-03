import React, { useState, useEffect } from "react";
import axios from "axios";
import { makeApiUrl } from "../api/apiConfig";
import PersonDropdown from "../components/common/PersonDropdown";

function RelationFinderPage() {
  console.log("RelationFinderPage RENDER");
  const [persons, setPersons] = useState([]);
  const [personA, setPersonA] = useState("");
  const [personB, setPersonB] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);


  // ================================================================
  // 🔹 Lấy danh sách person từ backend
  // ================================================================
  useEffect(() => {
    async function fetchPersons() {
      try {
        const res = await axios.get(
          makeApiUrl("/person/for-person-dropdown")
        )
        console.log("PERSON API RESPONSE", res.data);
        console.log("PERSON CÓ NĂM SINH", res.data.find(p => p.birth_date !== null));
        const personsActive = res.data;

        const sortedPersons = [...personsActive].sort((a, b) => {
          if (!a.birth_date && !b.birth_date) {
            return a.full_name_vn.localeCompare(b.full_name_vn, "vi");
          }

          if (!a.birth_date) return 1;
          if (!b.birth_date) return -1;

          if (a.birth_date !== b.birth_date) {
            return new Date(b.birth_date) - new Date(a.birth_date);
          }

          return a.full_name_vn.localeCompare(b.full_name_vn, "vi");
        });

        setPersons(sortedPersons);
      } catch (err) {
        console.error("❌ Lỗi khi tải danh sách:", err);
        setError("Không thể tải danh sách thành viên.");
      }
    }

    fetchPersons();
  }, []);
  // ================================================================
  // 🔹 Reset kết quả khi thay đổi lựa chọn
  // ================================================================
  useEffect(() => {
    setResult(null);
    setError("");
  }, [personA, personB]);
  // ================================================================
  // 🔹 Ghép họ tên
  // ================================================================
  const buildFullName = (p) => {
    return `${p.sur_name || ""} ${p.last_name || ""} ${p.middle_name || ""} ${p.first_name || ""
      }`
      .replace(/\s+/g, " ")
      .trim();
  };

  // ================================================================
  // 🔹 Gửi yêu cầu phân tích quan hệ
  // ================================================================
  const handleAnalyze = async () => {
    if (!personA || !personB) {
      setError("Vui lòng chọn đủ hai người để phân tích!");
      return;
    }

    if (personA === personB) {
      setError("Hai người không thể là cùng một cá nhân!");
      return;
    }

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const res = await axios.get(
        makeApiUrl(
          `/relationship?source_id=${parseInt(personB)}&target_id=${parseInt(personA)}`
        )
      );

      console.log("RELATION RESPONSE", res.data);
      setResult(res.data);
    } catch (err) {
      console.error("❌ Lỗi khi phân tích quan hệ:", err);
      setError("Đã xảy ra lỗi khi truy vấn máy chủ.");
    } finally {
      setLoading(false);
    }
  };


  // ================================================================
  // 🔹 Giao diện hiển thị
  // ================================================================
  const selectedA = persons.find(
    (p) => p.person_id === Number(personA)
  );

  const selectedB = persons.find(
    (p) => p.person_id === Number(personB)
  );
  return (
    <div className="max-w-2xl mx-auto bg-white/80 backdrop-blur-md shadow-lg rounded-2xl p-6 mt-10">
      <h1 className="text-2xl font-bold text-center text-indigo-700 mb-6">
        🔍 TÌM MỐI QUAN HỆ
      </h1>

      {/* Bộ chọn 2 người */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <PersonDropdown
          label="Người A:"
          value={personA}
          onChange={setPersonA}
          persons={persons}
          placeholder="-- Chọn Người A --"
        />

        <PersonDropdown
          label="Người B:"
          value={personB}
          onChange={setPersonB}
          persons={persons}
          placeholder="-- Chọn Người B --"
        />
      </div>

      {/* Nút phân tích */}
      <div className="text-center">
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className={`px-6 py-2 rounded-lg font-semibold text-white transition ${loading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700"
            }`}
        >
          {loading ? "Đang phân tích..." : "🔍 Phân Tích Quan Hệ"}
        </button>
      </div>

      {/* Kết quả */}

      {result && !error && (
        <div className="mt-6 text-center">
          <p className="p-4 bg-green-50 border border-green-300 rounded-lg text-green-700">
            <strong>
              {selectedA?.full_name_vn} là {result.relationship} của {selectedB?.full_name_vn}
            </strong>
          </p>

          {result.confidence && (
            <p className="mt-2 text-sm text-gray-500">
              Độ tin cậy: {result.confidence}
            </p>
          )}
        </div>
      )}

    </div>
  );
}

export default RelationFinderPage;
