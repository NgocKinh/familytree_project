import json


class RelationEngineV2:

    @staticmethod
    def classify(direction_path: str, gender_path: str, lineage_path: str, depth: int):

        direction_list, gender_list, lineage_list, depth = RelationEngineV2._parse_inputs(
            direction_path, gender_path, lineage_path, depth
        )

        if direction_list is None:
            return "không xác định"

        if not direction_list:
            return "bản thân"

        # Đếm số UP liên tiếp từ đầu
        a = 0
        for d in direction_list:
            if d == "UP":
                a += 1
            else:
                break

        b = len(direction_list) - a

        # Kiểm tra cấu trúc hợp lệ UP^a DOWN^b
        if direction_list != ["UP"] * a + ["DOWN"] * b:
            return "họ hàng xa"

        # ===== TỔ TIÊN =====
        if b == 0:
            return RelationEngineV2._handle_ancestor(a, gender_list, lineage_list)

        # ===== HẬU DUỆ =====
        if a == 0:
            return RelationEngineV2._handle_descendant(b, gender_list)

        # ===== BẢNG QUAN HỆ ĐỐI XỨNG (DEPTH ≤ 5) =====
        relation_map = {

            # 1-1: Anh chị em
            (1, 1): lambda: RelationEngineV2._handle_sibling(gender_list),

            # 2-1: Chú / Bác
            (2, 1): lambda: RelationEngineV2._handle_uncle_aunt(gender_list, lineage_list),

            # 1-2: Cháu (con của anh/chị/em)
            (1, 2): lambda: "cháu trai" if gender_list[-1] == "M" else "cháu gái",

            # 2-2: Anh chị em họ
            (2, 2): lambda: "anh/chị/em họ",

            # 3-1: Ông chú / ông bác
            (3, 1): lambda: RelationEngineV2._handle_grand_uncle_aunt(gender_list, lineage_list),

            # 1-3: Cháu gọi bằng ông
            (1, 3): lambda: "cháu trai gọi bằng ông"
                if gender_list[-1] == "M" else "cháu gái gọi bằng ông",

            # 3-2: Bà con họ
            (3, 2): lambda: RelationEngineV2._handle_uncle_aunt_cousin(
                gender_list, lineage_list
            ),
 
            # 2-3: Cháu họ
            (2, 3): lambda: "cháu họ",

            # 4-1: Cụ chú / cụ bác
            (4, 1): lambda: "cụ chú/cụ bác",

            # 1-4: Cháu gọi bằng cụ
            (1, 4): lambda: "cháu gọi bằng cụ",
        }

        key = (a, b)
        if key in relation_map:
            return relation_map[key]()

        return "họ hàng xa"
        
    # --------------------------
    # PARSE LAYER
    # --------------------------

    @staticmethod
    def _parse_inputs(direction_path, gender_path, lineage_path, depth):
        try:
            direction_list = json.loads(direction_path)
            gender_list = json.loads(gender_path)
            lineage_list = json.loads(lineage_path)
            depth = int(depth)
            return direction_list, gender_list, lineage_list, depth
        except Exception:
            return None, None, None, None


    # --------------------------
    # HELPER LAYER
    # --------------------------

    @staticmethod
    def _is_all(direction_list, value):
        return len(direction_list) > 0 and all(d == value for d in direction_list)

    # --------------------------
    # RULE LAYER
    # --------------------------

    @staticmethod
    def _handle_ancestor(depth, gender_list, lineage_list):
        gender = gender_list[-1] if gender_list else None

        # CHA / MẸ
        if depth == 1:
            return "cha" if gender == "M" else "mẹ"

        # ÔNG / BÀ (PHÂN BIỆT NỘI / NGOẠI)
        if depth == 2:
            side = lineage_list[0] if lineage_list else None

            if gender == "M":
                return "ông nội" if side == "P" else "ông ngoại"
            else:
                return "bà nội" if side == "P" else "bà ngoại"

        # CỐ
        if depth == 3:
            return "ông cố" if gender == "M" else "bà cố"
        if depth == 4:
            return "cụ tổ"
        return "tổ tiên"


    @staticmethod
    def _handle_descendant(depth, gender_list):
        gender = gender_list[-1] if gender_list else None

        if depth == 1:
            return "con trai" if gender == "M" else "con gái"

        if depth == 2:
            return "cháu trai" if gender == "M" else "cháu gái"

        if depth == 3:
            return "chắt trai" if gender == "M" else "chắt gái"

        if depth == 4:
            return "chút trai" if gender == "M" else "chút gái"
        
        return "hậu duệ"


    @staticmethod
    def _handle_sibling(gender_list):
        gender = gender_list[-1] if gender_list else None
        return "anh/em trai" if gender == "M" else "chị/em gái"

    @staticmethod
    def _handle_uncle_aunt(gender_list, lineage_list):
        gender = gender_list[-1] if gender_list else None
        side = lineage_list[0] if lineage_list else None

        # BÊN NỘI
        if side == "P":
            if gender == "M":
                return "chú/bác"
            else:
                return "cô"

        # BÊN NGOẠI
        if side == "M":
            if gender == "M":
                return "cậu"
            else:
                return "dì"

        return "họ hàng"

    @staticmethod
    def _handle_uncle_aunt_cousin(gender_list, lineage_list):
        gender = gender_list[-1] if gender_list else None
        side = lineage_list[0] if lineage_list else None

        # Bên nội
        if side == "P":
            if gender == "M":
                return "chú/bác họ"
            else:
                return "cô họ"

        # Bên ngoại
        if side == "M":
            if gender == "M":
                return "cậu họ"
            else:
                return "dì họ"

        return "họ hàng"
        
    @staticmethod
    def _handle_grand_uncle_aunt(gender_list, lineage_list):
        gender = gender_list[-1] if gender_list else None
        side = lineage_list[0] if lineage_list else None

        # BÊN NỘI
        if side == "P":
            if gender == "M":
                return "ông chú/ông bác"
            else:
                return "bà cô"

        # BÊN NGOẠI
        if side == "M":
            if gender == "M":
                return "ông cậu"
            else:
                return "bà dì"

        return "họ hàng xa"

    @staticmethod
    def is_ancestor(direction_path: str):
        try:
            direction_list = json.loads(direction_path)
        except Exception:
            return False

        return len(direction_list) > 0 and all(d == "UP" for d in direction_list)


    @staticmethod
    def is_descendant(direction_path: str):
        try:
            direction_list = json.loads(direction_path)
        except Exception:
            return False

        return len(direction_list) > 0 and all(d == "DOWN" for d in direction_list)

    @staticmethod
    def is_sibling(direction_path: str):
        """
        Sibling thường có pattern: ["UP", "DOWN"]
        """
        try:
            direction_list = json.loads(direction_path)
        except Exception:
            return False

        return direction_list == ["UP", "DOWN"]

