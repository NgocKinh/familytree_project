import pytest

from app.core.priority_conflict_engine import PriorityConflictEngine
from app.core.relationship_candidate import RelationshipCandidate, RelationType


def test_higher_priority_wins():
    engine = PriorityConflictEngine()

    spouse = RelationshipCandidate(
        name="vợ",
        type=RelationType.SPOUSE,
        priority=100
    )

    blood = RelationshipCandidate(
        name="họ hàng xa",
        type=RelationType.BLOOD,
        priority=50
    )

    result = engine.resolve([blood, spouse])

    assert result.name == "vợ"


def test_lower_priority_loses():
    engine = PriorityConflictEngine()

    affinity = RelationshipCandidate(
        name="con rể",
        type=RelationType.CHILD_AFFINITY,
        priority=90
    )

    blood = RelationshipCandidate(
        name="họ hàng xa",
        type=RelationType.BLOOD,
        priority=50
    )

    result = engine.resolve([blood, affinity])

    assert result.name == "con rể"


def test_tie_break_by_confidence():
    engine = PriorityConflictEngine()

    c1 = RelationshipCandidate(
        name="A",
        type=RelationType.BLOOD,
        priority=50,
        confidence=0.3
    )

    c2 = RelationshipCandidate(
        name="B",
        type=RelationType.BLOOD,
        priority=50,
        confidence=0.9
    )

    result = engine.resolve([c1, c2])

    assert result.name == "B"


def test_empty_candidate_returns_none():
    engine = PriorityConflictEngine()

    result = engine.resolve([])

    assert result is None
