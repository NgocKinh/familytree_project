from backend.services.family_tree_service import get_uncle_aunt_relationship
def test_uncle_aunt_valid(db, family_layer1):
    result = get_uncle_aunt_relationship(
        db,
        person_a_id=family_layer1["co"],
        person_b_id=family_layer1["con"]
    )
    assert result is not None
    assert result["relationship"] == "UNCLE_AUNT"


def test_uncle_aunt_invalid(db, family_layer1):
    result = get_uncle_aunt_relationship(
        db,
        person_a_id=family_layer1["stranger"],
        person_b_id=family_layer1["con"]
    )
    assert result is None
