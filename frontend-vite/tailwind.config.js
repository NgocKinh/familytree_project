/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // 🔹 Bộ sưu tập font thư pháp Việt (Google Fonts)
        greatvibes: ['"Great Vibes"', "cursive"],     // Cổ điển, mềm mại
        dancing: ['"Dancing Script"', "cursive"],     // Hiện đại, dễ đọc
        pacifico: ['"Pacifico"', "cursive"],          // Nghệ thuật, bay bổng
        parisienne: ['"Parisienne"', "cursive"],      // Thanh thoát, tinh tế
        sacramento: ['"Sacramento"', "cursive"],      // Mảnh nhẹ, sang trọng
      },

      // 🔹 Ảnh nền trang chủ
      backgroundImage: {
        trongdong: "url('/trongdong.png')",
      },
    },
  },
  plugins: [],
};


