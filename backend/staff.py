from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from models import db, Trek, Booking
from utils import role_required
from cache import cache_delete_pattern

staff_bp = Blueprint("staff", __name__)


# ---------------------------------------------------------
# View Assigned Treks
# ---------------------------------------------------------

@staff_bp.route("/treks", methods=["GET"])
@role_required("Trek Staff")
def assigned_treks():

    staff_id = int(get_jwt_identity())

    treks = Trek.query.filter_by(
        assigned_staff_id=staff_id
    ).all()

    return jsonify([trek.to_dict() for trek in treks])


# ---------------------------------------------------------
# Update Trek
# ---------------------------------------------------------

@staff_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@role_required("Trek Staff")
def update_trek_status(trek_id):

    staff_id = int(get_jwt_identity())

    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != staff_id:
        return jsonify({
            "message": "You are not assigned to this trek."
        }), 403

    data = request.get_json() or {}

    if "available_slots" in data:
        trek.available_slots = data["available_slots"]

    if "status" in data:

        allowed_statuses = [
            "Open",
            "Closed",
            "Started",
            "Completed"
        ]

        if data["status"] not in allowed_statuses:
            return jsonify({
                "message": "Invalid trek status."
            }), 400

        trek.status = data["status"]

    db.session.commit()

    cache_delete_pattern("treks:*")

    return jsonify({
        "message": "Trek updated successfully.",
        "trek": trek.to_dict()
    })


# ---------------------------------------------------------
# View Participants
# ---------------------------------------------------------

@staff_bp.route("/participants/<int:trek_id>", methods=["GET"])
@role_required("Trek Staff")
def view_participants(trek_id):

    staff_id = int(get_jwt_identity())

    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != staff_id:
        return jsonify({
            "message": "You are not assigned to this trek."
        }), 403

    bookings = Booking.query.filter_by(
        trek_id=trek_id,
        status="Booked"
    ).all()

    participants = []

    for booking in bookings:

        participants.append({
            "booking_id": booking.id,
            "user_id": booking.user.id,
            "user_name": booking.user.name,
            "user_email": booking.user.email,
            "phone": booking.user.phone,
            "booking_date": booking.booking_date.isoformat()
        })

    return jsonify(participants)