# Family Test Dataset

## 1. Mục đích
Dataset này dùng để:
- Test Tầng 1: quan hệ ruột (cha/mẹ, con, anh/em, ông/bà, chú/bác/cô/cậu/dì)
- Test Tầng 2: quan hệ họ (cousin, cô/chú/bác/cậu/dì họ, cháu họ, cousin bậc 2)
- Có giới tính đầy đủ để mở rộng sau này (ông nội / bà ngoại…)

Dataset này KHÔNG dùng cho production.

---

## 2. Quy ước
- Mọi logic suy luận dựa trên `person_id`
- `first_name` chỉ dùng để dễ đọc/test
- Tên đã được chuẩn hoá bằng chữ cái an toàn, không mang ý nghĩa huyết thống

---

## 3. Danh sách PERSON

| person_id | name | gender |
|-----------|------|--------|
| 96 | H | male |
| 97 | K | female |
| 98 | L | male |
| 99 | N | female |
| 100 | Q | male |
| 101 | R | female |
| 102 | T | female |
| 103 | V | female |
| 104 | X | male |
| 105 | Y | male |
| 106 | Z | male |
| 107 | D | female |
| 108 | E | male |
| 109 | I | female |
| 110 | J | male |
| 111 | O | female |
| 112 | W | female |
| 113 | B | female |
| 114 | U | male |
| 115 | S | male |

---

## 4. Quan hệ cha – con (parent_child)

### Family A
- 96 (H) + 97 (K) → 100 (Q), 102 (T)
- 98 (L) + 99 (N) → 101 (R)
- 100 (Q) + 101 (R) → 103 (V), 104 (X)

### Family B
- 106 (Z) + 107 (D) → 110 (J), 112 (W)
- 108 (E) + 109 (I) → 111 (O)
- 110 (J) + 111 (O) → 113 (B), 114 (U)

---

## 5. Các nhóm gia đình độc lập
- Family A: person_id 96–105
- Family B: person_id 106–115

Hai family này **không có quan hệ với nhau**, dùng để kiểm tra hệ thống không suy luận sai chéo family.

---

## 6. Test cases mong đợi (tham chiếu, chưa test)

### Tầng 1
- Q ↔ R : vợ/chồng
- Q ↔ V/X : cha – con
- V ↔ X : anh/em
- H/K ↔ V/X : ông/bà – cháu
- Q ↔ T : anh/em

### Tầng 2
- V ↔ (con của T) : cousin (nếu có thêm)
- Q ↔ (con của T) : chú/bác/cô/cậu/dì họ
- (con của Q) ↔ (con của J) : cousin bậc 2

(Danh sách này sẽ được cập nhật khi test thực tế)

---

## 7. Ghi chú
- Mọi thay đổi logic Tầng 1 / Tầng 2 phải đối chiếu lại README này
- Không chỉnh dữ liệu test khi chưa cập nhật README
