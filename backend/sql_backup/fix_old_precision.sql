-- ==============================================================
-- File: fix_old_precision.sql
-- Tác dụng:
--   ✅ Chuẩn hóa lại dữ liệu cũ trong bảng `person`
--   ✅ Gán giá trị đúng cho birth_date_precision và death_date_precision
--     dựa theo pattern ngày (nếu = 01/01 thì là 'year', nếu = 01 thì 'month')
-- Thời điểm chạy: CHỈ CHẠY 1 LẦN duy nhất trước khi kích hoạt trigger
--
-- Hướng dẫn chạy:
--   1️⃣ Mở MySQL Workbench
--   2️⃣ Chọn database: familytreedb
--   3️⃣ Bôi đen toàn bộ file này
--   4️⃣ Nhấn Ctrl + Enter để chạy
-- ==============================================================

USE familytreedb;

-- Chuẩn hóa birth_date_precision và death_date_precision cho dữ liệu cũ
UPDATE person
SET
  birth_date_precision =
    CASE
      WHEN birth_date IS NULL THEN birth_date_precision
      WHEN DAY(birth_date) = 1 AND MONTH(birth_date) = 1 THEN 'year'
      WHEN DAY(birth_date) = 1 THEN 'month'
      ELSE 'exact'
    END,
  death_date_precision =
    CASE
      WHEN death_date IS NULL THEN death_date_precision
      WHEN DAY(death_date) = 1 AND MONTH(death_date) = 1 THEN 'year'
      WHEN DAY(death_date) = 1 THEN 'month'
      ELSE 'exact'
    END
WHERE birth_date IS NOT NULL OR death_date IS NOT NULL;

-- Kiểm tra nhanh kết quả sau khi cập nhật
SELECT
    p.person_id,
    pc.father_id,
    pc.mother_id
FROM person p
LEFT JOIN parent_child pc
    ON p.person_id = pc.child_id
WHERE p.delete_status = 0
