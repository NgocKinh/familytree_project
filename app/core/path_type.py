from enum import Enum
import json


class PathType(str, Enum):
    LINEAR = "LINEAR"          # Cha, ông, con, cháu (chỉ lên hoặc chỉ xuống)
    COLLATERAL = "COLLATERAL"  # Chú, bác, anh họ (UP^a DOWN^b)
    AFFINAL = "AFFINAL"        # Quan hệ qua hôn nhân
    MIXED = "MIXED"            # Zigzag không thuần


def classify_path_type(direction_path: str) -> PathType:
    try:
        direction_list = json.loads(direction_path)
    except Exception:
        return PathType.MIXED

    if not direction_list:
        return PathType.LINEAR

    # Đếm UP liên tiếp đầu
    a = 0
    for d in direction_list:
        if d == "UP":
            a += 1
        else:
            break

    b = len(direction_list) - a

    # LINEAR (chỉ UP hoặc chỉ DOWN)
    if a == len(direction_list) or b == len(direction_list):
        return PathType.LINEAR

    # COLLATERAL (UP^a DOWN^b)
    if direction_list == ["UP"] * a + ["DOWN"] * b:
        return PathType.COLLATERAL

    # Còn lại là zigzag
    return PathType.MIXED