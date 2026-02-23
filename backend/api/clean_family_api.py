from flask import Blueprint, request, jsonify
from services.family_tree_service import create_child_from_marriage
from db import get_connection

clean_family_bp = Blueprint("clean_family", __name__, url_prefix="/api/clean")

@clean_family_bp.route("/child", methods=["POST"])
def create_child():
    data = request.json

    conn = get_connection()
    try:
        child_id = create_child_from_marriage(
            db=conn,
            marriage_id=data["marriage_id"],
            child_data=data["child"]
        )
        return jsonify({"child_id": child_id})
    finally:
        conn.close()
