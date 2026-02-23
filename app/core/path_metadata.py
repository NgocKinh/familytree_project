import json
from typing import Dict


def compute_path_metadata(direction_path: str) -> Dict:
    try:
        direction_list = json.loads(direction_path)
    except Exception:
        return {}

    if not direction_list:
        return {
            "generation_up": 0,
            "generation_down": 0,
            "generation_delta": 0,
            "blood_distance": 0,
            "is_linear": True,
            "is_collateral": False,
        }

    # Đếm UP liên tiếp đầu
    a = 0
    for d in direction_list:
        if d == "UP":
            a += 1
        else:
            break

    b = len(direction_list) - a

    is_linear = (a == len(direction_list)) or (b == len(direction_list))
    is_collateral = direction_list == ["UP"] * a + ["DOWN"] * b and a > 0 and b > 0

    return {
        "generation_up": a,
        "generation_down": b,
        "generation_delta": a - b,
        "blood_distance": a + b,
        "is_linear": is_linear,
        "is_collateral": is_collateral,
    }