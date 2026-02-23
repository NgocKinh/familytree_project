from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_spouse_overrides_blood():
    """
    Nếu vừa là spouse vừa có blood relation,
    spouse (priority 100) phải thắng.
    """

    response = client.get(
        "/relationship",
        params={"source_id": 96, "target_id": 97}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["relationship"] in ["vợ", "chồng"]


def test_reverse_spouse_direction():
    """
    Kiểm tra chiều ngược lại.
    """

    response = client.get(
        "/relationship",
        params={"source_id": 97, "target_id": 96}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["relationship"] in ["vợ", "chồng"]


def test_not_found_returns_404():
    """
    Nếu không có quan hệ gì,
    API phải trả 404.
    """

    response = client.get(
        "/relationship",
        params={"source_id": 999999, "target_id": 888888}
    )

    assert response.status_code == 404

def test_co_spouse_male_source():
    # source = nam, target = nam
    response = client.get(
        "/relationship",
        params={"source_id": 1, "target_id": 3}
    )
    assert response.status_code == 200
    assert response.json()["relationship"] in [
        "anh/em bạn rể",
        "chị/em bạn rể"
    ]


def test_co_spouse_female_source():
    # source = nữ, target = nữ
    response = client.get(
        "/relationship",
        params={"source_id": 2, "target_id": 4}
    )
    assert response.status_code == 200
    assert response.json()["relationship"] in [
        "anh/em bạn dâu",
        "chị/em bạn dâu"
    ]

def test_shared_spouse_relationship():
    response = client.get(
        "/relationship",
        params={"source_id": 5, "target_id": 6}
    )
    assert response.status_code == 200
    assert response.json()["relationship"] in [
        "vợ cùng chồng",
        "chồng cùng vợ"
    ]
