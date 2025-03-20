from app.models import User
from app.extensions import db

class UserService:
    @staticmethod
    def get_paginated_users(page, per_page):
        return User.query.paginate(page, per_page, False)
    
    @staticmethod
    def delete_user_by_email(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}
        
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}
    
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}
