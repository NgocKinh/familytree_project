README.md (hoàn chỉnh, có DB setup)
# Family Tree Project

Ứng dụng Gia Phả (Backend: Flask + MySQL, Frontend: React + Vite + Tailwind)

---

## 📌 Yêu cầu
- Python 3.13+
- PowerShell (Windows)
- MySQL 8+
- Node.js 22+
- npm 10+

---

## 🗄️ Chuẩn bị Database MySQL

Mở MySQL CLI hoặc Workbench và chạy:

```sql
-- 1. Tạo database
CREATE DATABASE IF NOT EXISTS familytreedb
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE familytreedb;

-- 2. Tạo bảng person (phiên bản cơ bản)
CREATE TABLE IF NOT EXISTS person (
    person_id INT AUTO_INCREMENT PRIMARY KEY,
    sur_name VARCHAR(100) NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100) NULL,
    first_name VARCHAR(100) NOT NULL,
    gender ENUM('male','female','other') NOT NULL,
    birth_date DATE NULL,
    death_date DATE NULL,
    birth_place VARCHAR(255) NULL,
    death_place VARCHAR(255) NULL,
    grave_info TEXT NULL,
    nationality VARCHAR(100) NULL,
    ethnic_group VARCHAR(100) NULL,
    religion VARCHAR(100) NULL,
    language_spoken VARCHAR(100) NULL,
    school_attended VARCHAR(255) NULL,
    degree_earned VARCHAR(255) NULL,
    address VARCHAR(255) NULL,
    phone_number VARCHAR(50) NULL,
    note TEXT NULL,
    delete_status TINYINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    deleted_at TIMESTAMP NULL
);


👉 Bảng person này đã đồng bộ với các API person_basic.py.

🚀 Cách chạy Backend

Mở PowerShell và gõ từng lệnh sau:

# 1. Điều hướng đến thư mục backend
cd C:\Users\RLappc.com\familytree_project\backend

# 2. Kích hoạt virtual environment
.\venv\Scripts\Activate.ps1

# 3. Cài đặt thư viện cần thiết (chỉ cần chạy lần đầu hoặc khi thêm thư viện mới)
pip install -r requirements.txt

# 4. Chạy Flask app
python app.py


Backend mặc định chạy tại:
👉 http://localhost:5000

🌐 Cách chạy Frontend (Vite + React + Tailwind)

Mở PowerShell mới và chạy:

# 1. Điều hướng đến thư mục frontend-vite
cd C:\Users\RLappc.com\familytree_project\frontend-vite

# 2. Cài đặt dependencies (chỉ cần lần đầu)
npm install

# 3. Chạy dev server
npm run dev


Frontend mặc định chạy tại:
👉 http://localhost:5173

📂 Cấu trúc thư mục
familytree_project/
├── backend/           # Flask backend + API
│   ├── api/           # Các blueprint API (person, line, relationship...)
│   ├── venv/          # Virtual environment (Python)
│   ├── app.py         # Flask app chính
│   └── requirements.txt
│
├── frontend-vite/     # React + Vite + Tailwind frontend
│   ├── src/           # Source code React
│   ├── index.html     # Entry point Vite
│   └── package.json
│
└── README.md          # Hướng dẫn dự án

⚙️ Ghi chú

Khi chạy dự án, cần mở 2 terminal:

1 terminal cho backend (python app.py)

1 terminal cho frontend (npm run dev)

Nếu MySQL không chạy được, hãy kiểm tra lại service MySQL80 trong Windows Services.

Sau khi có dữ liệu trong bảng person, bạn có thể quản lý qua PersonBasicForm hoặc