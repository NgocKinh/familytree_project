import React from "react";

function Home() {
  return (
    <div
      className="min-h-screen w-full bg-cover bg-center bg-no-repeat flex flex-col items-center justify-center text-center px-4"
      style={{ backgroundImage: "url('/trongdong.png')" }}
    >
      {/* ========================== */}
      {/* 🔹 TIÊU ĐỀ CHÍNH */}
      {/* ========================== */}
      <h1 className="font-sans text-6xl md:text-7xl font-bold text-red-600 drop-shadow-[2px_2px_0_#2563eb] mb-2">
        GIA PHẢ TỘC TRẦN
      </h1>

      {/* 🔹 Dòng chữ thư pháp */}
      <div className="mb-6 space-y-3">
        <h2 className="font-dancing text-5xl md:text-6xl text-red-700 drop-shadow-[2px_2px_0_#fbbf24]">
          Hào Khí Đông A
        </h2>
      </div>

      {/* 🔹 Slogan */}
      <p className="text-3xl md:text-4xl text-green-700 font-bold mb-3 drop-shadow-lg">
        Kết Nối Nghĩa Tình – Đời Đời Bền Vững
      </p>
      <p className="text-2xl md:text-4xl text-blue-700 font-semibold mb-10 drop-shadow-lg">
        Tộc Trần – An Quán - Thu Bồn
      </p>

      {/* ========================== */}
      {/* 🔹 THÔNG BÁO CHÀO MỪNG / HƯỚNG DẪN */}
      {/* ========================== */}
      <div className="bg-black bg-opacity-40 text-yellow-100 text-lg md:text-xl font-medium px-8 py-5 rounded-2xl shadow-lg max-w-3xl leading-relaxed">
        🌿 <b>Chào mừng bạn đến với hệ thống Gia Phả Tộc Trần</b> —  
        nơi lưu giữ truyền thống, kết nối các thế hệ và tôn vinh cội nguồn.
        <br />
        💡 Hãy sử dụng <b>thanh điều hướng phía trên</b> để xem danh sách thành viên,
        cây gia phả hoặc những thông tin mới.
      </div>

      {/* ========================== */}
      {/* 🔹 Ghi chú / mô tả phụ */}
      {/* ========================== */}
      <p className="mt-10 text-gray-200 italic text-sm bg-black bg-opacity-30 px-4 py-2 rounded-lg">
        Giao diện thử nghiệm – các chức năng đang trong quá trình hoàn thiện
      </p>
    </div>
  );
}

export default Home;














