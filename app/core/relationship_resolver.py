from typing import List
import json
from fastapi import HTTPException
from app.database import get_family_path, get_spouse_relationship
from app.relation_engine import RelationEngine
from app.relation_engine_v2 import RelationEngineV2
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
from app.core.blood_engine import BloodEngine
from app.core.relationship_candidate import RelationshipCandidate, RelationType
from app.core.priority_conflict_engine import PriorityConflictEngine
from app.core.affinity_engine import AffinityResolverEngine

class RelationshipResolver:

    def resolve(self, source_id: int, target_id: int) -> dict:
        print("RESOLVER VERSION TEST")
        candidates: List[RelationshipCandidate] = []

                # 1. Affinity relations (spouse + in-law)
        affinity_engine = AffinityResolverEngine()
        affinity_candidates = affinity_engine.resolve(source_id, target_id)
        candidates.extend(affinity_candidates)


        # 3. Blood relation
        blood_engine = BloodEngine()
        blood_candidates = blood_engine.resolve(source_id, target_id)
        candidates.extend(blood_candidates)
        print("CANDIDATES:", candidates)
        if not candidates:
            raise HTTPException(status_code=404, detail="Không tìm thấy quan hệ")
        print("DEBUG CANDIDATES:")
        for c in candidates:
            print(c.name, c.priority)
        engine = PriorityConflictEngine()
        best = engine.resolve(candidates)

        return {
            "source_id": source_id,
            "target_id": target_id,
            "relationship": best.name,
        }
    def _is_blood_pattern(self, direction_path: str) -> bool:
        try:
            direction_list = json.loads(direction_path)
        except Exception:
            return False

        a = 0
        for d in direction_list:
            if d == "UP":
                a += 1
            else:
                break

        b = len(direction_list) - a
        return direction_list == ["UP"] * a + ["DOWN"] * b

    def _check_symmetry(self, source_id: int, target_id: int):
        path_ab = get_family_path(source_id, target_id)
        path_ba = get_family_path(target_id, source_id)

        if not path_ab or not path_ba:
            return

        if not self._is_blood_pattern(path_ab["direction_path"]):
            return

        if not self._is_blood_pattern(path_ba["direction_path"]):
            return

        list_ab = json.loads(path_ab["direction_path"])
        list_ba = json.loads(path_ba["direction_path"])

        inverted_ba = list(
            reversed(["UP" if d == "DOWN" else "DOWN" for d in list_ba])
        )

        if list_ab != inverted_ba:
            print("⚠ SYMMETRY ERROR:",
                  source_id, target_id,
                  "AB:", list_ab,
                  "BA:", list_ba)

def invert_relationship(rel):
    mapping = {
        "chú/bác": "cháu",
        "cô/dì": "cháu",
        "ông": "cháu",
        "bà": "cháu",
        "cha": "con",
        "mẹ": "con",
        "con trai": "cha/mẹ",
        "con gái": "cha/mẹ",
    }
    return mapping.get(rel, rel)
