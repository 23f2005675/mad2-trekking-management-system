from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(*allowed_roles):
    """
    Restrict access to specific roles.

    Example:
        @role_required("Admin")
        @role_required("Admin", "Trek Staff")
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Verify JWT exists and is valid
            verify_jwt_in_request()

            claims = get_jwt()

            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": "You are not authorized to access this resource."
                }), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator