from werkzeug.security import check_password_hash
from zoneinfo import ZoneInfo
from ..models.user import User
from ..config import Config
from ..utils.logger import logger
from ..utils.token import TokenUtils

class AuthService:
    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("ユーザーが登録されていません")
        if not check_password_hash(user.password, password):
            raise ValueError("パスワードが違います")
        token = TokenUtils.generate_token(user.id)
        logger.info(f"{user.username}がログインしました")
        return {"access_token" : token}