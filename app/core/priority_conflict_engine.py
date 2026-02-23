from typing import List, Optional
from app.core.relationship_candidate import RelationshipCandidate


class PriorityConflictEngine:
    """
    Priority-based relationship conflict resolution engine.

    - Nhận danh sách RelationshipCandidate
    - Chọn candidate hợp lệ theo priority
    - Xử lý tie
    - Chuẩn bị mở rộng rule trong tương lai
    """

    def resolve(self, candidates: List[RelationshipCandidate]) -> Optional[RelationshipCandidate]:

        if not candidates:
            return None

        # Group theo priority
        priority_map = {}
        for candidate in candidates:
            priority_map.setdefault(candidate.priority, []).append(candidate)

        highest_priority = max(priority_map.keys())
        top_group = priority_map[highest_priority]

        # Nếu chỉ có 1 candidate ở priority cao nhất
        if len(top_group) == 1:
            return top_group[0]

        # Nếu có tie → resolve tie
        return self._resolve_tie(top_group)

    def _resolve_tie(self, candidates: List[RelationshipCandidate]) -> RelationshipCandidate:
        """
        Xử lý khi có nhiều candidate cùng priority.
        Hiện tại: chọn confidence cao nhất.
        Có thể mở rộng rule sau.
        """

        return max(candidates, key=lambda c: c.confidence)
