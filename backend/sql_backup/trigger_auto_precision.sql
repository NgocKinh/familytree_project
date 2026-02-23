-- ==============================================================
-- File: trigger_auto_precision.sql
-- Tác dụng:
--   ✅ Tự động xác định độ chính xác (precision) của birth_date / death_date
--      khi INSERT hoặc UPDATE vào bảng `person`
--   ✅ Không làm sai lệch ngày thật (vẫn giữ nguyên nếu nhập đủ ngày/tháng/năm)
--   ✅ Không cần chạy thủ công sau này, vì trigger sẽ tự hoạt động
--
-- Hướng dẫn chạy:
--   1️⃣ Mở MySQL Workbench
--   2️⃣ Chọn database: familytreedb
--   3️⃣ Bôi đen toàn bộ từ "USE familytreedb;" đến "DELIMITER ;"
--   4️⃣ Nhấn Ctrl + Shift + Enter để chạy toàn khối
-- ==============================================================

USE familytreedb;

-- Xóa trigger cũ nếu có (tránh lỗi trùng)
DROP TRIGGER IF EXISTS trg_auto_precision_insert;
DROP TRIGGER IF EXISTS trg_auto_precision_update;

DELIMITER //

-- Trigger khi INSERT
CREATE TRIGGER trg_auto_precision_insert
BEFORE INSERT ON person
FOR EACH ROW
BEGIN
  -- ====== BIRTH DATE ======
  IF NEW.birth_date IS NULL THEN
    SET NEW.birth_date_precision = 'unknown';
  ELSE
    IF DAY(NEW.birth_date) = 1 AND MONTH(NEW.birth_date) = 1 THEN
      SET NEW.birth_date_precision = 'year';
    ELSEIF DAY(NEW.birth_date) = 1 THEN
      SET NEW.birth_date_precision = 'month';
    ELSE
      SET NEW.birth_date_precision = 'exact';
    END IF;
  END IF;

  -- ====== DEATH DATE ======
  IF NEW.death_date IS NULL THEN
    SET NEW.death_date_precision = 'unknown';
  ELSE
    IF DAY(NEW.death_date) = 1 AND MONTH(NEW.death_date) = 1 THEN
      SET NEW.death_date_precision = 'year';
    ELSEIF DAY(NEW.death_date) = 1 THEN
      SET NEW.death_date_precision = 'month';
    ELSE
      SET NEW.death_date_precision = 'exact';
    END IF;
  END IF;
END;
//

-- Trigger khi UPDATE
CREATE TRIGGER trg_auto_precision_update
BEFORE UPDATE ON person
FOR EACH ROW
BEGIN
  -- ====== BIRTH DATE ======
  IF NEW.birth_date IS NULL THEN
    SET NEW.birth_date_precision = 'unknown';
  ELSE
    IF DAY(NEW.birth_date) = 1 AND MONTH(NEW.birth_date) = 1 THEN
      SET NEW.birth_date_precision = 'year';
    ELSEIF DAY(NEW.birth_date) = 1 THEN
      SET NEW.birth_date_precision = 'month';
    ELSE
      SET NEW.birth_date_precision = 'exact';
    END IF;
  END IF;

  -- ====== DEATH DATE ======
  IF NEW.death_date IS NULL THEN
    SET NEW.death_date_precision = 'unknown';
  ELSE
    IF DAY(NEW.death_date) = 1 AND MONTH(NEW.death_date) = 1 THEN
      SET NEW.death_date_precision = 'year';
    ELSEIF DAY(NEW.death_date) = 1 THEN
      SET NEW.death_date_precision = 'month';
    ELSE
      SET NEW.death_date_precision = 'exact';
    END IF;
  END IF;
END;
//
DELIMITER ;



