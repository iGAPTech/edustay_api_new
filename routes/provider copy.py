from flask import Blueprint, request
from db import get_db_connection
from utils.response import success

provider_bp = Blueprint("provider", __name__)

@provider_bp.route("/add-property", methods=["POST"])
def add_property():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO properties
        (provider_id, property_type_id, title, rent, deposit,
         address, latitude, longitude)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["provider_id"],
        data["property_type_id"],
        data["title"],
        data["rent"],
        data["deposit"],
        data["address"],
        data["latitude"],
        data["longitude"]
    ))

    conn.commit()
    cur.close()
    conn.close()

    return success("Property added. Waiting for admin approval")


# My Properties

@provider_bp.route("/my-properties/<int:provider_id>", methods=["GET"])
def my_properties(provider_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT * FROM properties
        WHERE provider_id=%s
    """, (provider_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()

    return success("My properties", data)

# Update Property

@provider_bp.route("/update-property", methods=["POST"])
def update_property():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE properties
        SET rent=%s, deposit=%s, address=%s
        WHERE id=%s
    """, (
        data["rent"],
        data["deposit"],
        data["address"],
        data["property_id"]
    ))

    conn.commit()
    cur.close()
    conn.close()

    return success("Property updated")

# Booking Requests

@provider_bp.route("/booking-requests/<int:provider_id>", methods=["GET"])
def booking_requests(provider_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT b.id, b.status, b.booking_date,
           b.payment_status, b.contact_shared,
           u.name as student_name, u.mobile,
           p.title
        FROM bookings b
        JOIN properties p ON b.property_id = p.id
        JOIN users u ON b.student_id = u.id
        WHERE p.provider_id = %s
        ORDER BY b.id DESC
    """, (provider_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()

    return success("Booking requests", data)

# Accept / Reject Booking

@provider_bp.route("/booking-action", methods=["POST"])
def booking_action():
    booking_id = request.json["booking_id"]
    status = request.json["status"]  # accepted / rejected

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE bookings
        SET status=%s
        WHERE id=%s
    """, (status, booking_id))

    conn.commit()
    cur.close()
    conn.close()

    return success("Booking status updated")
