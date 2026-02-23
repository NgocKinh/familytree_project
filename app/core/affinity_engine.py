from typing import List
from app.core.relationship_candidate import RelationshipCandidate, RelationType
from app.database import get_spouse_relationship
from app.affinity_repository import (
    is_co_spouse,
    is_parallel_sibling_in_law,
    is_son_in_law,
    is_daughter_in_law,
    is_brother_in_law,
    is_sister_in_law,
    is_parent_in_law,
    is_sibling_in_law_reverse,
)


class AffinityResolverEngine:

    def resolve(self, source_id: int, target_id: int) -> List[RelationshipCandidate]:
        candidates: List[RelationshipCandidate] = []

        # 1. Spouse
        spouse = get_spouse_relationship(source_id, target_id)
        if spouse:
            candidates.append(
                RelationshipCandidate(
                    name=spouse,
                    type=RelationType.SPOUSE,
                    priority=100,
                )
            )

        # 2. Co-spouse
        co_spouse = is_co_spouse(source_id, target_id)
        if co_spouse:
            candidates.append(
                RelationshipCandidate(
                    name=co_spouse,
                    type=RelationType.SIBLING_AFFINITY,
                    priority=85,
                )
            )

        # 3. Parallel sibling in-law
        parallel_in_law = is_parallel_sibling_in_law(source_id, target_id)
        if parallel_in_law:
            candidates.append(
                RelationshipCandidate(
                    name=parallel_in_law,
                    type=RelationType.SIBLING_AFFINITY,
                    priority=84,
                )
            )

        # 4. Child affinity
        if is_son_in_law(source_id, target_id):
            candidates.append(
                RelationshipCandidate(
                    name="con rể",
                    type=RelationType.CHILD_AFFINITY,
                    priority=90,
                )
            )

        if is_daughter_in_law(source_id, target_id):
            candidates.append(
                RelationshipCandidate(
                    name="con dâu",
                    type=RelationType.CHILD_AFFINITY,
                    priority=90,
                )
            )

        # 5. Sibling affinity
        if is_brother_in_law(source_id, target_id):
            candidates.append(
                RelationshipCandidate(
                    name="anh/em rể",
                    type=RelationType.SIBLING_AFFINITY,
                    priority=80,
                )
            )

        if is_sister_in_law(source_id, target_id):
            candidates.append(
                RelationshipCandidate(
                    name="chị/em dâu",
                    type=RelationType.SIBLING_AFFINITY,
                    priority=80,
                )
            )

        # 6. Parent in-law
        parent_in_law = is_parent_in_law(source_id, target_id)
        if parent_in_law:
            candidates.append(
                RelationshipCandidate(
                    name=parent_in_law,
                    type=RelationType.PARENT_IN_LAW,
                    priority=70,
                )
            )

        # 7. Reverse sibling in-law
        reverse = is_sibling_in_law_reverse(source_id, target_id)
        if reverse:
            candidates.append(
                RelationshipCandidate(
                    name=reverse,
                    type=RelationType.SIBLING_AFFINITY,
                    priority=80,
                )
            )

        return candidates