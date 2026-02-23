# backend/api/relationship_api.py
from flask import Blueprint, jsonify, request
from api.person_basic import get_person_basic_by_id
from presentation.relation_naming import invert_relation
from db import get_connection

relationship_api_bp = Blueprint(
    "relationship_api_bp",
    __name__,
    url_prefix="/api"
)


def get_gender(person_id):
    p = get_person_basic_by_id(person_id).get_json()
    return p.get("gender")


@relationship_api_bp.route("/relationship/find", methods=["POST"])
def find_relationship_api():
    data = request.get_json()
    from_id = data.get("from_person_id")
    to_id = data.get("to_person_id")

    if not from_id or not to_id:
        return jsonify({"status": "error"}), 400

    if from_id == to_id:
        return jsonify({"relation_basic": "Chính bản thân"})

    from services.family_tree_orchestrator import get_relationship_unified

    result = get_relationship_unified(
        db=get_connection(),
        person_a_id=from_id,
        person_b_id=to_id
    )

    return jsonify(result)
