from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
from utils.response import success, error

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # 🔹 Check if mobile already exists
    cur.execute("SELECT id FROM users WHERE mobile=%s", (data["mobile"],))
    existing_user = cur.fetchone()

    if existing_user:
        cur.close()
        conn.close()
        return error("Mobile number already registered")

    # 🔹 Insert new user
    cur.execute("""
        INSERT INTO users (name, email, mobile, password, role, gender)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["name"],
        data.get("email"),
        data["mobile"],
        generate_password_hash(data["password"]),
        data["role"],
        data["gender"]
    ))

    conn.commit()
    cur.close()
    conn.close()

    return success("Registration successful")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE mobile=%s", (data["mobile"],))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user and check_password_hash(user["password"], data["password"]):
        return success("Login successful", {
            "user_id": user["id"],
            "role": user["role"],
            "name": user["name"],
            "gender": user["gender"]
        })

    return error("Invalid credentials")
