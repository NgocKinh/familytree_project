# ============================================================
# MOCK RELATIONSHIP DATA & ENGINE
# Dùng để test logic quan hệ (KHÔNG DB, KHÔNG FLASK)
# ============================================================

# =========================
# MOCK DATA
# =========================

# Giới tính
# id -> "male" | "female"
MOCK_GENDER = {
    1: "female",   # A
    2: "female",   # B
    3: "male",     # X (chồng của B)
}

MOCK_PARENT_CHILD = {
    3: [1],        # A là MẸ của X
}

MOCK_MARRIAGE = {
    2: [3],        # B cưới X
    3: [2],
}

# =========================
# MOCK HELPERS
# =========================

def mock_get_gender(person_id):
    return MOCK_GENDER.get(person_id)

def mock_get_parents(child_id):
    return MOCK_PARENT_CHILD.get(child_id, [])

def mock_get_spouses(person_id):
    return MOCK_MARRIAGE.get(person_id, [])

# =========================
# MOCK BLOOD RELATION ENGINE
# (đơn giản: chỉ xét CHA / MẸ)
# =========================

def find_blood_relation(A_id, B_id):
    """
    Trả về: 'Cha', 'Mẹ' hoặc None
    """
    parents = mock_get_parents(B_id)
    if A_id in parents:
        gender = mock_get_gender(A_id)
        return "Cha" if gender == "male" else "Mẹ"
    return None

# =========================
# MAIN MOCK ENGINE
# A là gì của B ?
# Theo flow 3 bước + vòng lặp multi-spouse
# =========================

def find_relationship_mock(A_id, B_id):
    """
    Trả về:
    - Cha
    - Mẹ
    - Cha chồng / Cha vợ
    - Mẹ chồng / Mẹ vợ
    - Không xác định
    """

    # BƯỚC 1: HUYẾT THỐNG TRỰC TIẾP A -> B
    direct = find_blood_relation(A_id, B_id)
    if direct:
        return direct

    # BƯỚC 2: HÔN NHÂN CỦA B (đa hôn)
    spouses = mock_get_spouses(B_id)

    # BƯỚC 3: LẶP TỪNG PHỐI NGẪU X
    for X_id in spouses:
        rel_AX = find_blood_relation(A_id, X_id)
        if not rel_AX:
            continue

        X_gender = mock_get_gender(X_id)

        if rel_AX == "Cha":
            return "Cha chồng" if X_gender == "male" else "Cha vợ"
        else:  # Mẹ
            return "Mẹ chồng" if X_gender == "male" else "Mẹ vợ"

    return "Không xác định"

# =========================
# SIMPLE TEST
# =========================

if __name__ == "__main__":
    # A = 1 (cha của X1)
    # B = 2 (cưới X1 và X2)

    print(find_relationship_mock(1, 2))