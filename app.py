import os
from datetime import date, datetime, timedelta, timezone

import jwt
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from menu_routes import menu_bp
from models import db, User, UserRole
import fill

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://app:app@db:5432/app"
)


def create_app():
    app = Flask(__name__, static_folder="public", static_url_path="")

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        fill.seed_test_data(date(2026, 2, 9), days=10)

    app.register_blueprint(menu_bp)

    def make_token(user):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "login": user.login,
            "role": user.role.name,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=JWT_EXPIRES_MINUTES)).timestamp()),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    @app.get("/")
    def index():
        return send_from_directory(app.static_folder, "login.html")

    # Страницы
    @app.get("/login")
    def login_page():
        return send_from_directory(app.static_folder, "login.html")

    @app.get("/register")
    def register_page():
        return send_from_directory(app.static_folder, "register.html")

    # ДОБАВЛЕНО:
    # универсальная раздача всех статических файлов
    # styles.css, vegetables.png, js, fonts и т.д.
    @app.get("/<path:filename>")
    def static_files(filename):
        return send_from_directory(app.static_folder, filename)

    @app.post("/register")
    def register():
        data = request.get_json(silent=True) or {}

        login = (data.get("login") or "").strip().lower()
        password = data.get("password") or ""

        if not login or not password:
            return {"message": "login и password обязательны"}, 400

        if User.query.filter_by(login=login).first():
            return {"message": "Пользователь уже существует"}, 409

        user = User(
            login=login,
            password_hash=generate_password_hash(password),
            role=UserRole.STUDENT,
            money=0
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "Регистрация успешна"}, 201

    @app.post("/login")
    def login():
        data = request.get_json(silent=True) or {}

        login = (data.get("login") or "").strip().lower()
        password = data.get("password") or ""

        user = User.query.filter_by(login=login).first()

        if not user or not check_password_hash(user.password_hash, password):
            return {"message": "Неверный login или пароль"}, 401

        token = make_token(user)

        return jsonify({
            "token": token,
            "token_type": "Bearer",
            "expires_in_minutes": JWT_EXPIRES_MINUTES
        })

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)