from flask import Blueprint, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from zoneinfo import ZoneInfo
from ..models.user import User
from ..services.auth import AuthService
from app.database import db
from app.utils.response import success_response, error_response
from ..config import Config
from ..utils.logger import logger

class UserService:
    @staticmethod
    def register(username, email, password):
        if User.query.filter_by(email=email).first():
            raise ValueError("このメールアドレスは登録されています")
        hashed = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        logger.info(f"{username}の登録が完了しました")
        return user