from flask_jwt_extended import create_access_token
from datetime import timedelta, datetime
from app.models import User
from app.extensions import db

class AuthService:
    @staticmethod
    def generate_token(user_id):
        return create_access_token(identity=str(user_id), expires_delta=timedelta(days=1))

    @staticmethod
    def register_user(email: str, firstname: str, lastname: str, phone: str, password: str):
        email = email.strip().lower()
        if User.query.filter_by(email=email).first():
            return {"error": "User already exists"}

        user = User(email=email, firstname=firstname, lastname=lastname, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully", "data": {} }

    @staticmethod
    def authenticate_user(email, password):
        email = email.strip().lower()
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return { "error": "Invalid credentials" }

        token = AuthService.generate_token(user.id)
        return {
            "data": {"access_token": token},
            "message": "User authenticated successfully"
        }
