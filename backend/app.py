from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

from config import Config
from models import db, User

from auth import auth_bp
from admin import admin_bp
from user import user_bp
from staff import staff_bp

from tasks import init_celery


def create_default_admin():
    """
    Create the default admin account if it does not already exist.
    """

    admin = User.query.filter_by(
        email="admin@trek.com"
    ).first()

    if admin:
        return

    admin = User(
        name="Admin",
        email="admin@trek.com",
        password_hash=generate_password_hash(
            "admin123",
            method="pbkdf2:sha256"
        ),
        role="Admin",
        is_active=True,
        is_blacklisted=False
    )

    db.session.add(admin)
    db.session.commit()

    print("=" * 60)
    print("Default Admin Created")
    print("Email    : admin@trek.com")
    print("Password : admin123")
    print("=" * 60)


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)

    JWTManager(app)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*"
            }
        }
    )

    # Register Blueprints
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        admin_bp,
        url_prefix="/api/admin"
    )

    app.register_blueprint(
        user_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        staff_bp,
        url_prefix="/api/staff"
    )

    with app.app_context():

        db.create_all()

        create_default_admin()

    # Initialize Celery
    init_celery(app)

    @app.route("/")
    def home():

        return jsonify({
            "project": "Trekking Management System",
            "status": "Running"
        })

    @app.route("/api/health")
    def health():

        return jsonify({
            "status": "Healthy"
        })

    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )