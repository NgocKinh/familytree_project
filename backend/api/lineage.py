from flask import Blueprint, request, jsonify
from db import get_connection

lineage_bp = Blueprint("lineage_bp", __name__)

ALLOWED_FIELDS = ["name", "original_place"]

# GET all lineages
@lineage_bp.route("/", methods=["GET"])
def list_lineages():
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM lineage")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(rows)

# GET one lineage
@lineage_bp.route("/<int:lid>", methods=["GET"])
def get_lineage(lid):
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM lineage WHERE id=%s", (lid,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        return jsonify({"error": "Lineage not found"}), 404
    return jsonify(row)

# CREATE
@lineage_bp.route("/", methods=["POST"])
def create_lineage():
    data = request.json or {}
    cols = [c for c in ALLOWED_FIELDS if c in data]
    if not cols:
        return jsonify({"error": "No fields to insert"}), 400
    placeholders = ", ".join(["%s"] * len(cols))
    sql = f"INSERT INTO lineage ({', '.join(cols)}) VALUES ({placeholders})"
    vals = [data.get(c) for c in cols]

    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, tuple(vals)); conn.commit()
    new_id = cur.lastrowid
    cur.close(); conn.close()
    return jsonify({"id": new_id}), 201

# UPDATE
@lineage_bp.route("/<int:lid>", methods=["PUT"])
def update_lineage(lid):
    data = request.json or {}
    cols = [c for c in ALLOWED_FIELDS if c in data]
    if not cols:
        return jsonify({"message": "Nothing to update"}), 400
    sets = ", ".join([f"{c}=%s" for c in cols])
    sql = f"UPDATE lineage SET {sets} WHERE id=%s"
    vals = [data.get(c) for c in cols] + [lid]

    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, tuple(vals)); conn.commit()
    cur.close(); conn.close()
    return jsonify({"message": "updated"})

# DELETE (xóa hẳn)
@lineage_bp.route("/<int:lid>", methods=["DELETE"])
def delete_lineage(lid):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM lineage WHERE id=%s", (lid,))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({"message": "deleted"})
