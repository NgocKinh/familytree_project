import json


class RelationEngine:

    @staticmethod
    def classify(direction_path: str, gender_path: str, lineage_path: str, depth: int):

        direction_list, gender_list, lineage_list, depth = RelationEngine._parse_inputs(
            direction_path, gender_path, lineage_path, depth
        )

        if direction_list is None:
            return "không xác định"

        # Layer 1: self
        if depth == 0:
            return "bản thân"

        # Layer 2: thuần UP
        if RelationEngine._is_all(direction_list, "UP"):
            return RelationEngine._handle_ancestor(depth, gender_list, lineage_list)

        # Layer 3: thuần DOWN
        if RelationEngine._is_all(direction_list, "DOWN"):
            return RelationEngine._handle_descendant(depth, gender_list)

        # Layer 4: sibling
        if direction_list == ["UP", "DOWN"]:
            return RelationEngine._handle_sibling(gender_list)

        # Layer 5: uncle/aunt
        if direction_list.count("UP") == 2 and direction_list.count("DOWN") == 1:
            return RelationEngine._handle_uncle_aunt(
                gender_list,
                lineage_list
            )

        # GRAND UNCLE / GRAND AUNT
        if direction_list.count("UP") == 3 and direction_list.count("DOWN") == 1:
            return RelationEngine._handle_grand_uncle_aunt(
                gender_list,
                lineage_list
            )

        # COUSIN
        if direction_list.count("UP") == 2 and direction_list.count("DOWN") == 2:
            return "anh/chị/em họ"

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

        if depth == 5:
            return "chít trai" if gender == "M" else "chít gái"

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

