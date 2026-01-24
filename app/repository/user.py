from flask import session
from ..database import db
from ..models.user import User

class UserRepository:
    def get_user_by_mail(self, email):
        return User.query.filter_by(email=email).first()

    def register(self, username, email, password):
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user