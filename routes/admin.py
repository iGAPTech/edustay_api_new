from flask import Blueprint, request
from db import get_db_connection
from utils.response import success, error

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/approve-property", methods=["POST"])
def approve_property():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE properties
        SET status='approved'
        WHERE id=%s
    """, (data["property_id"],))

    conn.commit()
    cur.close()
    conn.close()

    return success("Property approved")

# All Users

@admin_bp.route("/users", methods=["GET"])
def users():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT id,name,mobile,role,status FROM users")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return success("Users list", data)

# Students List
@admin_bp.route("/students", methods=["GET"])
def students():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT id,name,mobile,role,status FROM users WHERE role='student'")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return success("Students list", data)

# Providers List
# @admin_bp.route("/providers", methods=["GET"])
# def providers():
#     conn = get_db_connection()
#     cur = conn.cursor(dictionary=True)

#     cur.execute("SELECT id,name,mobile,role,status FROM users WHERE role='provider'")
#     data = cur.fetchall()

#     cur.close()
#     conn.close()
#     return success("Providers list", data)

@admin_bp.route("/providers", methods=["GET"])
def providers():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT u.id, u.name, u.mobile, u.role, u.status,
            CASE 
                WHEN p.user_id IS NULL THEN 'no_profile'
                ELSE p.is_verified
            END as is_verified
        FROM users u
        LEFT JOIN provider_profiles p ON u.id = p.user_id
        WHERE u.role = 'provider'
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return success("Providers list", data)

@admin_bp.route("/change-verify-status", methods=["POST"])
def change_verify_status():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if record exists
    cur.execute("SELECT id FROM provider_profiles WHERE user_id=%s", (data["user_id"],))
    exists = cur.fetchone()

    if exists:
        # Update
        cur.execute("""
            UPDATE provider_profiles
            SET is_verified=%s
            WHERE user_id=%s
        """, (data["is_verified"], data["user_id"]))
    else:
        # Insert (IMPORTANT FIX)
        cur.execute("""
            INSERT INTO provider_profiles (user_id, is_verified)
            VALUES (%s, %s)
        """, (data["user_id"], data["is_verified"]))

    conn.commit()
    cur.close()
    conn.close()

    return success("Verification updated")

@admin_bp.route("/change-status", methods=["POST"])
def change_user_status():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET status=%s WHERE id=%s",
        (data["status"], data["user_id"])
    )

    conn.commit()
    cur.close()
    conn.close()

    return success("Status updated successfully")



# Block User

@admin_bp.route("/block-user", methods=["POST"])
def block_user():
    user_id = request.json["user_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users SET status='blocked'
        WHERE id=%s
    """, (user_id,))

    conn.commit()
    cur.close()
    conn.close()

    return success("User blocked")

# Pending Properties

@admin_bp.route("/pending-properties", methods=["GET"])
def pending_properties():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT * FROM properties
        WHERE status='pending'
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()

    return success("Pending properties", data)

# Reject Properties

@admin_bp.route("/reject-property", methods=["POST"])
def reject_property():
    property_id = request.json["property_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE properties
        SET status='rejected'
        WHERE id=%s
    """, (property_id,))

    conn.commit()
    cur.close()
    conn.close()

    return success("Property rejected")

# -------------------------------
# Admin: Approve / Reject Property
# -------------------------------
@admin_bp.route("/update-property-status", methods=["POST"])
def update_property_status():

    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE properties
        SET status=%s
        WHERE id=%s
    """, (data["status"], data["property_id"]))

    conn.commit()
    cur.close()
    conn.close()

    return success("Status updated")



@admin_bp.route("/all-properties", methods=["GET"])
def all_properties():

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT p.*, u.name as provider_name
        FROM properties p
        JOIN users u ON p.provider_id = u.id
        ORDER BY p.id DESC
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return success("All properties", data)


@admin_bp.route("/property-details/<int:property_id>", methods=["GET"])
def property_details(property_id):

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # Property
    cur.execute("""
        SELECT p.*, u.name as provider_name, u.mobile
        FROM properties p
        JOIN users u ON p.provider_id = u.id
        WHERE p.id=%s
    """, (property_id,))
    property_data = cur.fetchone()

    # Images
    cur.execute("SELECT image FROM property_images WHERE property_id=%s", (property_id,))
    images = cur.fetchall()

    # Facilities
    cur.execute("""
        SELECT f.facility_name
        FROM property_facilities pf
        JOIN facilities f ON pf.facility_id = f.id
        WHERE pf.property_id=%s
    """, (property_id,))
    facilities = cur.fetchall()

    return success("Details", {
        "property": property_data,
        "images": images,
        "facilities": facilities
    })



@admin_bp.route("/bookings", methods=["GET"])
def admin_bookings():

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT b.*, p.title, u.name as student_name
        FROM bookings b
        JOIN properties p ON b.property_id = p.id
        JOIN users u ON b.student_id = u.id
        ORDER BY b.id DESC
    """)

    data = cur.fetchall()

    return success("Bookings", data)

@admin_bp.route("/reports", methods=["GET"])
def admin_reports():

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # 1️⃣ Total Earnings
    cur.execute("SELECT IFNULL(SUM(payment_amount),0) as total FROM bookings WHERE payment_status='paid'")
    total_earnings = cur.fetchone()["total"]

    # 2️⃣ Total Bookings
    cur.execute("SELECT COUNT(*) as total FROM bookings")
    total_bookings = cur.fetchone()["total"]

    # 3️⃣ Total Students
    cur.execute("SELECT COUNT(*) as total FROM users WHERE role='student'")
    total_students = cur.fetchone()["total"]

    # 4️⃣ Total Providers
    cur.execute("SELECT COUNT(*) as total FROM users WHERE role='provider'")
    total_providers = cur.fetchone()["total"]

    # 5️⃣ Monthly Earnings
    cur.execute("""
        SELECT MONTH(created_at) as month, SUM(payment_amount) as amount
        FROM bookings
        WHERE payment_status='paid'
        GROUP BY MONTH(created_at)
    """)
    monthly = cur.fetchall()

    # 6️⃣ Booking Status Count
    cur.execute("""
        SELECT status, COUNT(*) as count
        FROM bookings
        GROUP BY status
    """)
    status = cur.fetchall()

    cur.close()
    conn.close()

    return success("Report Data", {
        "total_earnings": total_earnings,
        "total_bookings": total_bookings,
        "total_students": total_students,
        "total_providers": total_providers,
        "monthly": monthly,
        "status": status
    })



# 
