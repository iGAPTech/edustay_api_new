from flask import Blueprint, request
from db import get_db_connection
from utils.response import success, error
import os, time
from werkzeug.utils import secure_filename

provider_bp = Blueprint("provider", __name__)



# -------------------------------
# Add Property (Room / PG / Hostel / Mess)
# -------------------------------
@provider_bp.route("/add-property", methods=["POST"])
def add_property():
    data = request.json

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO properties
            (provider_id, property_type_id, title, description,
             rent, deposit, total_capacity, available_capacity,
             address, latitude, longitude, gender_allowed)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data["provider_id"],
            data["property_type_id"],
            data["title"],
            data.get("description"),
            data["rent"],
            data.get("deposit"),
            data.get("total_capacity"),
            data.get("available_capacity"),
            data["address"],
            data["latitude"],
            data["longitude"],
            data.get("gender_allowed", "any")
        ))

        conn.commit()
        cur.close()
        conn.close()

        return success("Property added successfully. Waiting for admin approval")

    except Exception as e:
        return error(str(e))


UPLOAD_FOLDER = "uploads/property"

# @provider_bp.route("/upload-property-image", methods=["POST"])
# def upload_property_image():
#     property_id = request.form.get("property_id")
#     file = request.files.get("image")

#     if not file:
#         return error("No file selected")

#     filename = secure_filename(file.filename)
#     filepath = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(filepath)

#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         INSERT INTO property_images (property_id, image)
#         VALUES (%s,%s)
#     """, (property_id, filename))

#     conn.commit()
#     cur.close()
#     conn.close()

#     return success("Image uploaded")

# @provider_bp.route("/upload-property-image", methods=["POST"])
# def upload_property_image():
#     property_id = request.form.get("property_id")
#     image = request.files.get("image")

#     if not image:
#         return error("No image")

#     filename = f"{int(time.time())}_{image.filename}"
#     image.save(f"uploads/properties/{filename}")

#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         INSERT INTO property_images (property_id, image)
#         VALUES (%s, %s)
#     """, (property_id, filename))

#     conn.commit()
#     cur.close()
#     conn.close()

#     return success("Image uploaded")

UPLOAD_FOLDER = "uploads/properties"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

@provider_bp.route("/upload-property-image", methods=["POST"])
def upload_property_image():
    property_id = request.form.get("property_id")
    image = request.files.get("image")

    if not property_id:
        return error("Property ID is required")

    if not image:
        return error("No image file provided")

    if image.filename == "":
        return error("Empty filename")

    ext = image.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return error("Invalid image type")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(image.filename)
    filename = f"{int(time.time())}_{filename}"

    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO property_images (property_id, image) VALUES (%s, %s)",
        (property_id, filename)
    )

    conn.commit()
    cur.close()
    conn.close()

    return success("Image uploaded successfully")


@provider_bp.route("/property-images/<int:property_id>", methods=["GET"])
def property_images(property_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM property_images WHERE property_id=%s", (property_id,))
    data = cur.fetchall()

    cur.close()
    conn.close()
    return success("Images list", data)


@provider_bp.route("/delete-property-image", methods=["POST"])
def delete_property_image():
    image_id = request.json["image_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM property_images WHERE id=%s", (image_id,))
    conn.commit()

    cur.close()
    conn.close()
    return success("Image deleted")

# -------------------------------
# My Properties (Provider)
# -------------------------------
@provider_bp.route("/my-properties/<int:provider_id>", methods=["GET"])
def my_properties(provider_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT p.*, pt.type_name
        FROM properties p
        JOIN property_types pt ON p.property_type_id = pt.id
        WHERE p.provider_id=%s
        ORDER BY p.created_at DESC
    """, (provider_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()

    return success("My properties", data)


# -------------------------------
# Update Property
# -------------------------------
@provider_bp.route("/update-property", methods=["POST"])
def update_property():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    # Optional values (safe handling)
    description = data.get("description")
    total_capacity = data.get("total_capacity")
    available_capacity = data.get("available_capacity")

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    # 🧠 If lat/lng = 0 → ignore update
    if latitude == 0:
        latitude = None
    if longitude == 0:
        longitude = None

    cur.execute("""
        UPDATE properties
        SET title=%s,
            description=%s,
            rent=%s,
            deposit=%s,
            total_capacity=IFNULL(%s, total_capacity),
            available_capacity=IFNULL(%s, available_capacity),
            address=%s,
            latitude=IFNULL(%s, latitude),
            longitude=IFNULL(%s, longitude),
            gender_allowed=%s
        WHERE id=%s AND provider_id=%s
    """, (
        data["title"],
        description,
        data["rent"],
        data["deposit"],
        total_capacity,
        available_capacity,
        data["address"],
        latitude,
        longitude,
        data["gender_allowed"],
        data["property_id"],
        data["provider_id"]
    ))

    conn.commit()
    cur.close()
    conn.close()

    return success("Property updated successfully")

# -------------------------------
# Delete Property
# -------------------------------
@provider_bp.route("/delete-property", methods=["POST"])
def delete_property():
    property_id = request.json["property_id"]
    provider_id = request.json["provider_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM properties
        WHERE id=%s AND provider_id=%s
    """, (property_id, provider_id))

    conn.commit()
    cur.close()
    conn.close()

    return success("Property deleted successfully")


# -------------------------------
# Booking Requests for Provider
# -------------------------------
@provider_bp.route("/bookings/<provider_id>", methods=["GET"])
def provider_bookings(provider_id):

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

    return success("Provider bookings", data)


# -------------------------------
# Accept / Reject Booking
# -------------------------------
@provider_bp.route("/update-booking-status", methods=["POST"])
def update_booking_status():

    data = request.json
    booking_id = data["booking_id"]
    status = data["status"]

    conn = get_db_connection()
    cur = conn.cursor()

    if status == "accepted":
        cur.execute("""
            UPDATE bookings 
            SET status=%s, contact_shared='yes'
            WHERE id=%s
        """, (status, booking_id))

    else:
        cur.execute("""
            UPDATE bookings 
            SET status=%s, contact_shared='no'
            WHERE id=%s
        """, (status, booking_id))

    conn.commit()
    cur.close()
    conn.close()

    return success("Booking updated")

@provider_bp.route("/property-types", methods=["GET"])
def property_types():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT id,type_name FROM property_types")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return success("Property Type list", data)

@provider_bp.route("/facilities", methods=["GET"])
def facilities():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM facilities")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return success("Facilities list", data)

@provider_bp.route("/property-facilities/<int:property_id>", methods=["GET"])
def property_facilities(property_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT facility_id
        FROM property_facilities
        WHERE property_id=%s
    """, (property_id,))

    data = cur.fetchall()
    cur.close()
    conn.close()

    return success("Property facilities", data)


@provider_bp.route("/save-property-facilities", methods=["POST"])
def save_property_facilities():
    property_id = request.json["property_id"]
    facility_ids = request.json["facility_ids"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM property_facilities WHERE property_id=%s", (property_id,))

    for fid in facility_ids:
        cur.execute("""
            INSERT INTO property_facilities (property_id, facility_id)
            VALUES (%s,%s)
        """, (property_id, fid))

    conn.commit()
    cur.close()
    conn.close()

    return success("Facilities updated")

@provider_bp.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT u.name, u.email, u.mobile,
               p.address, p.id_proof, p.is_verified
        FROM users u
        LEFT JOIN provider_profiles p ON u.id = p.user_id
        WHERE u.id=%s
    """, (user_id,))

    data = cur.fetchone()

    cur.close()
    conn.close()

    return success("Profile fetched", data)
    


@provider_bp.route("/update-profile", methods=["POST"])
def update_profile():
    data = request.json

    user_id = data.get("user_id")
    address = data.get("address")

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if exists
    cur.execute("SELECT id FROM provider_profiles WHERE user_id=%s", (user_id,))
    existing = cur.fetchone()

    if existing:
        cur.execute("""
            UPDATE provider_profiles
            SET address=%s
            WHERE user_id=%s
        """, (address, user_id))
    else:
        cur.execute("""
            INSERT INTO provider_profiles (user_id, address)
            VALUES (%s, %s)
        """, (user_id, address))

    conn.commit()
    cur.close()
    conn.close()

    return success("Profile updated")


UPLOAD_FOLDER1 = "uploads/proofs"
os.makedirs(UPLOAD_FOLDER1, exist_ok=True)

@provider_bp.route("/upload-proof", methods=["POST"])
def upload_id_proof():
    user_id = request.form.get("user_id")

    if 'file' not in request.files:
        return error("No file uploaded")

    file = request.files['file']
    filename = secure_filename(file.filename)

    filename = f"id_{user_id}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER1, filename)
    file.save(filepath)

    conn = get_db_connection()
    cur = conn.cursor()

    # Check profile exists
    cur.execute("SELECT id FROM provider_profiles WHERE user_id=%s", (user_id,))
    profile = cur.fetchone()

    if profile:
        cur.execute("""
            UPDATE provider_profiles
            SET id_proof=%s
            WHERE user_id=%s
        """, (filename, user_id))
    else:
        cur.execute("""
            INSERT INTO provider_profiles (user_id, id_proof, is_verified)
            VALUES (%s, %s, 0)
        """, (user_id, filename))

    conn.commit()
    cur.close()
    conn.close()

    return success("ID proof uploaded successfully")


@provider_bp.route("/earnings/<int:provider_id>", methods=["GET"])
def provider_earnings(provider_id):

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # 1️⃣ Total Earnings
    cur.execute("""
        SELECT IFNULL(SUM(b.payment_amount),0) as total_earnings
        FROM bookings b
        JOIN properties p ON b.property_id = p.id
        WHERE p.provider_id=%s AND b.payment_status='paid'
    """, (provider_id,))
    total = cur.fetchone()

    # 2️⃣ Total Paid Bookings
    cur.execute("""
        SELECT COUNT(*) as total_bookings
        FROM bookings b
        JOIN properties p ON b.property_id = p.id
        WHERE p.provider_id=%s AND b.payment_status='paid'
    """, (provider_id,))
    count = cur.fetchone()

    # 3️⃣ Monthly Earnings
    cur.execute("""
        SELECT 
            MONTH(b.created_at) as month,
            SUM(b.payment_amount) as amount
        FROM bookings b
        JOIN properties p ON b.property_id = p.id
        WHERE p.provider_id=%s AND b.payment_status='paid'
        GROUP BY MONTH(b.created_at)
    """, (provider_id,))
    monthly = cur.fetchall()

    # 4️⃣ Recent Transactions
    cur.execute("""
        SELECT b.id, b.payment_amount, b.transaction_id,
               b.created_at, u.name as student_name, p.title
        FROM bookings b
        JOIN properties p ON b.property_id = p.id
        JOIN users u ON b.student_id = u.id
        WHERE p.provider_id=%s AND b.payment_status='paid'
        ORDER BY b.id DESC LIMIT 10
    """, (provider_id,))
    transactions = cur.fetchall()

    cur.close()
    conn.close()

    return success("Earnings data", {
        "total_earnings": total["total_earnings"],
        "total_bookings": count["total_bookings"],
        "monthly": monthly,
        "transactions": transactions
    })





