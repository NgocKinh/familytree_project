from app.database import get_family_path
from app.relation_engine_v2 import RelationEngineV2
from app.core.relationship_candidate import RelationshipCandidate, RelationType


class BloodEngine:

    def resolve(self, source_id: int, target_id: int):
        candidates = []

        path = get_family_path(source_id, target_id)

        if not path:
            return candidates

        relationship = RelationEngineV2.classify(
            path["direction_path"],
            path["gender_path"],
            path["lineage_path"],
            path["depth"],
        )

        blood_priority = 50

        normalized = (relationship or "").strip().lower()
        if "họ hàng xa" in normalized:
            blood_priority = 0

        candidates.append(
            RelationshipCandidate(
                name=relationship,
                type=RelationType.BLOOD,
                priority=blood_priority,
                metadata={
                    "direction_path": path["direction_path"],
                    "gender_path": path["gender_path"],
                    "lineage_path": path["lineage_path"],
                    "depth": path["depth"],
                },
            )
        )

        return candidates