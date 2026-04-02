from flask import Blueprint, request
from db import get_db_connection
from utils.response import error, success

student_bp = Blueprint("student", __name__)

@student_bp.route("/properties", methods=["GET"])
def get_properties():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT p.*, pt.type_name
        FROM properties p
        JOIN property_types pt ON p.property_type_id = pt.id
        WHERE p.status='approved'
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()

    return success("Properties fetched", data)


@student_bp.route("/book", methods=["POST"])
def book_property():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO bookings (student_id, property_id)
        VALUES (%s,%s)
    """, (data["student_id"], data["property_id"]))

    conn.commit()
    cur.close()
    conn.close()

    return success("Booking request sent")


# Property Details
@student_bp.route("/property/<int:property_id>", methods=["GET"])
def property_details(property_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT p.*, pt.type_name
        FROM properties p
        JOIN property_types pt ON p.property_type_id = pt.id
        WHERE p.id=%s AND p.status='approved'
    """, (property_id,))

    data = cur.fetchone()
    cur.close()
    conn.close()

    if not data:
        return error("Property not found")

    return success("Property details", data)

# Search Properties (Location + Filters)

@student_bp.route("/search", methods=["GET"])
def search_properties():
    lat = float(request.args.get("lat"))
    lng = float(request.args.get("lng"))
    max_rent = request.args.get("max_rent", 10000)

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT *,
        (6371 * acos(
            cos(radians(%s)) * cos(radians(latitude)) *
            cos(radians(longitude) - radians(%s)) +
            sin(radians(%s)) * sin(radians(latitude))
        )) AS distance
        FROM properties
        WHERE rent <= %s AND status='approved'
        HAVING distance <= 5
        ORDER BY distance
    """, (lat, lng, lat, max_rent))

    data = cur.fetchall()
    cur.close()
    conn.close()

    return success("Search results", data)

# My Bookings

@student_bp.route("/my-bookings/<int:student_id>", methods=["GET"])
def my_bookings(student_id):

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT b.*, p.title, p.address, u.mobile as provider_mobile
        FROM bookings b
        JOIN properties p ON p.id = b.property_id
        JOIN users u ON u.id = p.provider_id 
        WHERE b.student_id=%s
        ORDER BY b.created_at DESC
    """, (student_id,))

    data = cur.fetchall()

    cur.close()
    conn.close()

    return success("My bookings", data)

# Cancel Booking

@student_bp.route("/cancel-booking", methods=["POST"])
def cancel_booking():
    booking_id = request.json["booking_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE bookings
        SET status='cancelled'
        WHERE id=%s
    """, (booking_id,))

    conn.commit()
    cur.close()
    conn.close()

    return success("Booking cancelled")

# new 

@student_bp.route("/nearby-properties", methods=["POST"])
def nearby_properties():
    data = request.json
    lat = float(data["latitude"])
    lng = float(data["longitude"])

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            p.*,
            pt.type_name,

            -- Get one image
            (
                SELECT image 
                FROM property_images pi 
                WHERE pi.property_id = p.id 
                LIMIT 1
            ) AS main_image,

            (6371 * acos(
                cos(radians(%s)) *
                cos(radians(p.latitude)) *
                cos(radians(p.longitude) - radians(%s)) +
                sin(radians(%s)) *
                sin(radians(p.latitude))
            )) AS distance

        FROM properties p
        JOIN property_types pt ON pt.id = p.property_type_id

        WHERE p.status = 'approved' OR p.status='pending'
        HAVING distance < 40
        ORDER BY distance ASC
    """, (lat, lng, lat))

    result = cur.fetchall()
    cur.close()
    conn.close()

    return success("Nearby properties", result)


@student_bp.route("/property-details/<int:property_id>", methods=["GET"])
def property_detail(property_id):

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # Property
    cur.execute("""
        SELECT p.*, pt.type_name
        FROM properties p
        JOIN property_types pt ON pt.id = p.property_type_id
        WHERE p.id=%s
    """, (property_id,))
    property_data = cur.fetchone()

    # Images
    cur.execute("""
        SELECT image FROM property_images
        WHERE property_id=%s
    """, (property_id,))
    images = cur.fetchall()

    # Facilities
    cur.execute("""
        SELECT f.facility_name
        FROM property_facilities pf
        JOIN facilities f ON f.id = pf.facility_id
        WHERE pf.property_id=%s
    """, (property_id,))
    facilities = cur.fetchall()

    cur.close()
    conn.close()

    return success("Property details", {
        "property": property_data,
        "images": images,
        "facilities": facilities
    })


@student_bp.route("/book-property", methods=["POST"])
def book_property1():

    data = request.json
    student_id = data["student_id"]
    property_id = data["property_id"]
    payment_amount = data["payment_amount"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO bookings (student_id, property_id, payment_amount, booking_date, status)
        VALUES (%s, %s, %s, CURDATE(),  'requested')
    """, (student_id, property_id, payment_amount))

    conn.commit()
    cur.close()
    conn.close()

    return success("Booking request sent")

@student_bp.route("/make-payment", methods=["POST"])
def make_payment():
    data = request.json

    booking_id = data["booking_id"]
    amount = data["amount"]
    txn_id = data["transaction_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE bookings
        SET payment_status='paid',
            payment_amount=%s,
            transaction_id=%s
        WHERE id=%s
    """, (amount, txn_id, booking_id))

    conn.commit()
    cur.close()
    conn.close()

    return success("Payment successful")

@student_bp.route("/add-review", methods=["POST"])
def add_review():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reviews (student_id, property_id, rating, review)
        VALUES (%s, %s, %s, %s)
    """, (
        data["student_id"],
        data["property_id"],
        data["rating"],
        data["review"]
    ))

    conn.commit()
    cur.close()
    conn.close()

    return success("Review added")


@student_bp.route("/property-reviews/<int:property_id>")
def property_reviews(property_id):

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT r.*, u.name
        FROM reviews r
        JOIN users u ON u.id = r.student_id
        WHERE property_id=%s
    """, (property_id,))

    data = cur.fetchall()

    cur.close()
    conn.close()

    return success("Reviews", data)

@student_bp.route("/profile/<int:user_id>", methods=["GET"])
def get_student_profile(user_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT u.name, u.email, u.mobile,
               sp.college_name, sp.city, sp.aadhar_number, sp.pan_number
        FROM users u
        LEFT JOIN student_profiles sp
        ON u.id = sp.user_id
        WHERE u.id = %s
    """, (user_id,))

    data = cur.fetchone()

    cur.close()
    conn.close()

    return success("Profile data", data)

@student_bp.route("/update-profile", methods=["POST"])
def update_student_profile():
    data = request.json

    user_id = data.get("user_id")
    college = data.get("college_name")
    city = data.get("city")
    aadhar = data.get("aadhar_number")
    pan = data.get("pan_number")

    conn = get_db_connection()
    cur = conn.cursor()

    
    # Check if profile exists
    cur.execute("SELECT id FROM student_profiles WHERE user_id=%s", (user_id,))
    existing = cur.fetchone()

    if existing:
        cur.execute("""
            UPDATE student_profiles
            SET college_name=%s, city=%s, aadhar_number=%s, pan_number=%s
            WHERE user_id=%s
        """, (college, city, aadhar,pan, user_id))
    else:
        cur.execute("""
            INSERT INTO student_profiles
            (user_id, college_name, city, aadhar_number, pan_number)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, college, city,aadhar,pan ))

    conn.commit()
    cur.close()
    conn.close()

    return success("Profile updated")


# @student_bp.route("/nearby-properties", methods=["POST"])
# def nearby_properties():
#     data = request.json
#     lat = float(data["latitude"])
#     lng = float(data["longitude"])

#     conn = get_db_connection()
#     cur = conn.cursor(dictionary=True)

#     # Haversine formula (distance in KM)
#     cur.execute("""
#         SELECT p.*, pt.type_name,
#         (6371 * acos(
#             cos(radians(%s)) *
#             cos(radians(p.latitude)) *
#             cos(radians(p.longitude) - radians(%s)) +
#             sin(radians(%s)) *
#             sin(radians(p.latitude))
#         )) AS distance
#         FROM properties p
#         JOIN property_types pt ON pt.id = p.property_type_id
#         WHERE p.status='approved' OR p.status='pending'
#         HAVING distance < 20
#         ORDER BY distance ASC
#     """, (lat, lng, lat))

#     data = cur.fetchall()
#     cur.close()
#     conn.close()

#     return success("Nearby properties", data)


