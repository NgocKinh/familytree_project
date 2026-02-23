def present_relation(
    info: dict,
    gender: str | None = None,
    is_spouse_side: bool = False
) -> str:
    """
    PRESENTATION — EDGE-BASED (Y4)

    Input:
        info: {"direction": ..., "generation": int}
        gender: "male" | "female" | None
        is_spouse_side: dùng ở Y5 (chưa dùng ở Y4)

    Output:
        label (str)

    ❌ Không suy luận
    ❌ Không nội / ngoại
    ❌ Không đảo chiều
    """

    direction = info.get("direction")
    generation = info.get("generation", 0)

    # ===== SPOUSE =====
    if direction == "SPOUSE":
        if gender == "male":
            return "Chồng"
        if gender == "female":
            return "Vợ"
        return "Vợ/Chồng"

    # ===== UP =====
    if direction == "UP":
        if generation == 1:
            if gender == "male":
                return "Cha"
            if gender == "female":
                return "Mẹ"
            return "Cha/Mẹ"

        if generation == 2:
            title = "Ông" if gender == "male" else "Bà"
            side = "nội" if info.get("lineage_type") == "PATERNAL" else "ngoại"
            return f"{title} {side}"

        if generation == 3:
            if gender == "male":
                return "Ông cố"
            if gender == "female":
                return "Bà cố"
            return "Ông/Bà cố"

        if generation >= 4:
            return "Tổ tiên"
    
    # ===== DOWN =====
    if direction == "DOWN":
        lineage = info.get("lineage_type")

        if generation == 1:
            return "Con"


    # ===== SIDE =====
    if direction == "SIDE":
        return "Họ hàng ngang"

    return "Không xác định"


# ===== IN-LAW PARENT INVERTED MAP =====
INLAW_PARENT_INVERTED_MAP = {
    "Cha chồng": "Con dâu",
    "Mẹ chồng": "Con dâu",
    "Cha vợ": "Con rể",
    "Mẹ vợ": "Con rể",
}

def invert_relation(label: str) -> str:
    """
    PRESENTATION — INVERT (Y5)

    Đảo chiều nhãn quan hệ xã hội đã được present ở Y4.
    ❌ Không suy luận
    ❌ Không DB
    ❌ Không phụ thuộc core
    """

    if not label:
        return label

    # ===== IN-LAW (ƯU TIÊN TRƯỚC) =====
    INLAW_INVERT = {
        "Cha chồng": "Con dâu",
        "Mẹ chồng": "Con dâu",
        "Cha vợ": "Con rể",
        "Mẹ vợ": "Con rể",
        "Con dâu": "Cha/Mẹ chồng",
        "Con rể": "Cha/Mẹ vợ",
    }
    if label in INLAW_INVERT:
        return INLAW_INVERT[label]

    # ===== HÔN NHÂN =====
    if label == "Chồng":
        return "Vợ"
    if label == "Vợ":
        return "Chồng"

    # ===== TRỰC HỆ (ĐỐI XỨNG) =====
    DIRECT_INVERT = {
        "Cha": "Con",
        "Mẹ": "Con",
        "Con": "Cha/Mẹ",

        "Ông": "Cháu",
        "Bà": "Cháu",
        "Cháu": "Ông/Bà",

        "Ông cố": "Cháu cố",
        "Bà cố": "Cháu cố",
        "Cháu cố": "Ông/Bà cố",

        "Tổ tiên": "Hậu duệ",
        "Hậu duệ": "Tổ tiên",

        "Họ hàng ngang": "Họ hàng ngang",
    }

    return DIRECT_INVERT.get(label, label)
