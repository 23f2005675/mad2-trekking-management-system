import csv
import io

from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, User, Trek, Booking
from cache import cache_get, cache_set, cache_delete_pattern

user_bp = Blueprint("user", __name__)


# ---------------------------------------------------------
# Browse Treks
# ---------------------------------------------------------

@user_bp.route("/treks", methods=["GET"])
def list_open_treks():

    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")
    location = request.args.get("location", "")

    cache_key = f"treks:{search}:{difficulty}:{location}"

    cached = cache_get(cache_key)

    if cached:
        return jsonify(cached)

    query = Trek.query.filter_by(status="Open")

    if search:
        query = query.filter(Trek.name.ilike(f"%{search}%"))

    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    if location:
        query = query.filter(Trek.location.ilike(f"%{location}%"))

    treks = [trek.to_dict() for trek in query.all()]

    cache_set(cache_key, treks, ttl=60)

    return jsonify(treks)


@user_bp.route("/treks/<int:trek_id>", methods=["GET"])
def trek_details(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    return jsonify(trek.to_dict())


# ---------------------------------------------------------
# Booking
# ---------------------------------------------------------

@user_bp.route("/bookings", methods=["POST"])
@jwt_required()
def create_booking():

    user_id = int(get_jwt_identity())

    user = User.query.get_or_404(user_id)

    if user.role != "User":
        return jsonify({
            "message": "Only users can book treks."
        }), 403

    if user.is_blacklisted or not user.is_active:
        return jsonify({
            "message": "Your account is inactive."
        }), 403

    data = request.get_json() or {}

    trek = Trek.query.get_or_404(data.get("trek_id"))

    if trek.status != "Open":
        return jsonify({
            "message": "Trek is not open for booking."
        }), 400

    if trek.available_slots <= 0:
        return jsonify({
            "message": "No slots available."
        }), 400

    existing = Booking.query.filter_by(
        user_id=user.id,
        trek_id=trek.id,
        status="Booked"
    ).first()

    if existing:
        return jsonify({
            "message": "You have already booked this trek."
        }), 400

    booking = Booking(
        user_id=user.id,
        trek_id=trek.id,
        status="Booked",
        payment_status="Pending"
    )

    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    cache_delete_pattern("treks:*")

    return jsonify(booking.to_dict()), 201


# ---------------------------------------------------------
# Booking History
# ---------------------------------------------------------

@user_bp.route("/bookings/history", methods=["GET"])
@jwt_required()
def booking_history():

    user_id = int(get_jwt_identity())

    bookings = Booking.query.filter_by(
        user_id=user_id
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return jsonify([b.to_dict() for b in bookings])


# ---------------------------------------------------------
# Cancel Booking
# ---------------------------------------------------------

@user_bp.route("/bookings/<int:booking_id>", methods=["DELETE"])
@jwt_required()
def cancel_booking(booking_id):

    user_id = int(get_jwt_identity())

    booking = Booking.query.filter_by(
        id=booking_id,
        user_id=user_id
    ).first_or_404()

    if booking.status == "Cancelled":
        return jsonify({
            "message": "Booking already cancelled."
        }), 400

    booking.status = "Cancelled"

    booking.trek.available_slots += 1

    db.session.commit()

    cache_delete_pattern("treks:*")

    return jsonify({
        "message": "Booking cancelled successfully."
    })


# ---------------------------------------------------------
# Export CSV
# ---------------------------------------------------------

@user_bp.route("/bookings/export", methods=["GET"])
@jwt_required()
def export_booking_history():

    user_id = int(get_jwt_identity())

    bookings = Booking.query.filter_by(
        user_id=user_id
    ).all()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Booking ID",
        "Trek",
        "Booking Date",
        "Status",
        "Payment Status"
    ])

    for booking in bookings:

        writer.writerow([
            booking.id,
            booking.trek.name,
            booking.booking_date,
            booking.status,
            booking.payment_status
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=booking_history.csv"
        }
    )


# ---------------------------------------------------------
# Async Export
# ---------------------------------------------------------

@user_bp.route("/bookings/export/async", methods=["POST"])
@jwt_required()
def export_booking_history_async():

    from tasks import export_booking_history_task

    user_id = int(get_jwt_identity())

    task = export_booking_history_task.delay(user_id)

    return jsonify({
        "task_id": task.id,
        "message": "Export started."
    }), 202


# ---------------------------------------------------------
# Update Profile
# ---------------------------------------------------------

@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    user = User.query.get_or_404(
        int(get_jwt_identity())
    )

    data = request.get_json() or {}

    if "name" in data:
        user.name = data["name"]

    if "phone" in data:
        user.phone = data["phone"]

    db.session.commit()

    return jsonify(user.to_dict())