from flask import Blueprint, request, jsonify
from services.family_tree_service import create_child_from_marriage
from db import get_db

family_bp = Blueprint("family", __name__)

@family_bp.route("/child", methods=["POST"])
def create_child():
    data = request.json

    db = get_db()

    child_id = create_child_from_marriage(
        db=db,
        marriage_id=data["marriage_id"],
        child_data=data["child"]
    )

    return jsonify({"child_id": child_id})
