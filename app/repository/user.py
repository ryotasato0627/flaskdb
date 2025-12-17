from flask import session
from ..database import db
from ..models.user import User

class UserRepository:
    def get_user_by_mail(self, email):
        return User.qyery.filter_by(email=email).first()
    
    def create_user(self, username, email, password):
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        return user