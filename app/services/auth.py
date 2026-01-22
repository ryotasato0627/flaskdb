from flask import request
from werkzeug.security import check_password_hash
from ..repository.user import UserRepository
from ..utils.logger import logger
from ..utils.token import TokenUtils

class AuthService:
    @staticmethod
    def login(email, password):
        user = UserRepository().get_user_by_mail(email=email)
        if not user:
            raise ValueError("ユーザーが登録されていません")
        if not check_password_hash(user.password, password):
            raise ValueError("パスワードが違います")
        token = TokenUtils.generate_token(user.id)
        logger.info(f"{user.username}がログインしました")
        return {"access_token" : token}