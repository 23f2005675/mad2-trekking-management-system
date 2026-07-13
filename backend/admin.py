from datetime import datetime

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from models import db, User, StaffProfile, Trek, Booking
from utils import role_required
from cache import cache_delete_pattern

admin_bp = Blueprint("admin", __name__)


def parse_date(date_string):
    """Convert YYYY-MM-DD string to Python date."""
    if not date_string:
        return None

    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        return None


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

@admin_bp.route("/dashboard", methods=["GET"])
@role_required("Admin")
def dashboard():

    return jsonify({
        "total_users": User.query.filter_by(role="User").count(),
        "total_staff": User.query.filter_by(role="Trek Staff").count(),
        "total_treks": Trek.query.count(),
        "total_bookings": Booking.query.count()
    })


# ---------------------------------------------------------
# User Management
# ---------------------------------------------------------

@admin_bp.route("/users", methods=["GET"])
@role_required("Admin")
def list_users():

    users = User.query.filter_by(role="User").all()

    return jsonify([u.to_dict() for u in users])


@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
@role_required("Admin")
def update_user(user_id):

    user = User.query.filter_by(
        id=user_id,
        role="User"
    ).first_or_404()

    data = request.get_json() or {}

    if "is_blacklisted" in data:
        user.is_blacklisted = data["is_blacklisted"]

    db.session.commit()

    return jsonify(user.to_dict())


# ---------------------------------------------------------
# Staff Management
# ---------------------------------------------------------

@admin_bp.route("/staff", methods=["GET"])
@role_required("Admin")
def list_staff():

    staff = User.query.filter_by(role="Trek Staff").all()

    return jsonify([s.to_dict() for s in staff])


@admin_bp.route("/staff", methods=["POST"])
@role_required("Admin")
def create_staff():

    data = request.get_json() or {}

    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({
            "message": "Name, Email and Password are required."
        }), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({
            "message": "Email already exists."
        }), 400

    user = User(
        name=data["name"],
        email=data["email"].lower(),
        password_hash=generate_password_hash(
            data["password"],
            method="pbkdf2:sha256"
        ),
        phone=data.get("phone"),
        role="Trek Staff",
        is_active=True,
        is_blacklisted=False
    )

    db.session.add(user)
    db.session.flush()

    profile = StaffProfile(
        user_id=user.id,
        contact=data.get("contact"),
        status="Active"
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@admin_bp.route("/staff/<int:staff_id>", methods=["PUT"])
@role_required("Admin")
def update_staff(staff_id):

    staff = User.query.filter_by(
        id=staff_id,
        role="Trek Staff"
    ).first_or_404()

    data = request.get_json() or {}

    if "is_active" in data:
        staff.is_active = data["is_active"]

        if staff.staff_profile:
            staff.staff_profile.status = (
                "Active"
                if data["is_active"]
                else "Suspended"
            )

    if "is_blacklisted" in data:
        staff.is_blacklisted = data["is_blacklisted"]

    db.session.commit()

    return jsonify(staff.to_dict())


# ---------------------------------------------------------
# Trek Management
# ---------------------------------------------------------

@admin_bp.route("/treks", methods=["GET"])
@role_required("Admin")
def list_treks():

    treks = Trek.query.order_by(
        Trek.created_at.desc()
    ).all()

    return jsonify([t.to_dict() for t in treks])


@admin_bp.route("/treks", methods=["POST"])
@role_required("Admin")
def create_trek():

    data = request.get_json() or {}

    trek = Trek(
        name=data.get("name"),
        location=data.get("location"),
        difficulty=data.get("difficulty"),
        duration_days=data.get("duration_days"),
        description=data.get("description"),
        price=data.get("price", 0),
        available_slots=data.get("available_slots", 0),
        start_date=parse_date(data.get("start_date")),
        end_date=parse_date(data.get("end_date")),
        status="Pending"
    )

    db.session.add(trek)
    db.session.commit()

    cache_delete_pattern("treks:*")

    return jsonify(trek.to_dict()), 201


@admin_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@role_required("Admin")
def update_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    data = request.get_json() or {}

    editable_fields = [
        "name",
        "location",
        "difficulty",
        "duration_days",
        "description",
        "price",
        "available_slots",
        "status"
    ]

    for field in editable_fields:
        if field in data:
            setattr(trek, field, data[field])

    if "start_date" in data:
        trek.start_date = parse_date(data["start_date"])

    if "end_date" in data:
        trek.end_date = parse_date(data["end_date"])

    if "assigned_staff_id" in data:
        trek.assigned_staff_id = data["assigned_staff_id"]

    db.session.commit()

    cache_delete_pattern("treks:*")

    return jsonify(trek.to_dict())


@admin_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
@role_required("Admin")
def delete_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)
    db.session.commit()

    cache_delete_pattern("treks:*")

    return jsonify({
        "message": "Trek deleted successfully."
    })