"""
Relationship Orchestrator (B7)

Chiến lược:
- Ưu tiên V2 (ground truth sạch)
- Nếu V2 không xác định → fallback V1
- Không thay đổi V1/V2
"""

import backend.services.family_tree_service as v1
import backend.services.family_tree_cousin_v2 as v2


def get_relationship_unified(db, person_a_id: int, person_b_id: int) -> dict:
    """
    Orchestrator:
    - V2 trước
    - fallback V1
    """


    # 1️⃣ Thử V2
    result_v2 = v2.get_relationship_v2(db, person_a_id, person_b_id)

    if (
        result_v2
        and result_v2.get("relationship") not in ("UNDETERMINED", "DISABLED")
    ):
        return result_v2

    # 2️⃣ Fallback sang V1
    return v1.get_relationship(
        db,
        person_a_id,
        person_b_id,
        enable_theorem=True
    )
