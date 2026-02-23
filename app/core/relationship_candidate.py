from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any


class RelationType(Enum):
    SPOUSE = "spouse"
    CHILD_AFFINITY = "child_affinity"
    SIBLING_AFFINITY = "sibling_affinity"
    PARENT_IN_LAW = "parent_in_law"
    BLOOD = "blood"


@dataclass
class RelationshipCandidate:
    """
    Đại diện cho một khả năng quan hệ giữa 2 người.
    Dùng cho Priority-based Conflict Engine.
    """

    name: str
    type: RelationType
    priority: int
    confidence: float = 1.0
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type.value,
            "priority": self.priority,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }
