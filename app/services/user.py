from flask import Blueprint, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.user import User
from ..database import db
from ..repository.user import UserRepository
from ..utils.logger import logger


class UserService:
    def __init__(self, user_repo: UserRepository ):
        self.user_repo = user_repo

    def register(self, username, email, password):
        if self.user_repo.get_user_by_mail(email=email):
            raise ValueError("このメールアドレスは登録されています")
        hashed = generate_password_hash(password)
        user = self.user_repo.register(username=username, email=email, password=hashed)
        db.session.commit()
        logger.info(f"{username}の登録が完了しました")
        return user