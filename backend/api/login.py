print(">>> login.py LOADED <<<")
from flask import Blueprint, request, jsonify
import jwt
import datetime
import mysql.connector
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_SECONDS
from permissions import ROLE_KEYS

login_bp = Blueprint("login", __name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Msand@167",
        database="familytreedb"
    )

@login_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
       return jsonify({"ok": True}), 200
    data = request.get_json(force=True)
    print("RAW:", request.data)
    print("JSON:", data)
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT user_id, person_id, username, password_hash, role, status
        FROM user_account
        WHERE username = %s
        LIMIT 1
    """, (username,))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    if user["status"] != "active":
        return jsonify({"error": "User inactive"}), 403

    # ⚠️ TẠM THỜI so sánh plaintext (sẽ nâng cấp bcrypt sau)
    if password != user["password_hash"]:
        return jsonify({"error": "Invalid username or password"}), 401
    
    now = datetime.datetime.utcnow()
    
    keys = ROLE_KEYS.get(user["role"], [])

    payload = {
        "sub": user["user_id"],
        "role": user["role"],
        "person_id": user["person_id"],
        "keys": keys,          # ✅ DÒNG MỚI
        "iat": ...,
        "exp": ...
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return jsonify({
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"],
        "person_id": user["person_id"]
    })
