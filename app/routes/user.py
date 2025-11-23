from flask import Blueprint, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
from zoneinfo import ZoneInfo
from ..models.user import User
from app.database import db
from app.utils.response import success_response, error_response
from ..config import Config
from ..utils.logger import logger

user_bp = Blueprint('user', __name__, url_prefix="/user")

@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if User.query.filter_by(email=data["email"]):
        return error_response("登録済みのemailです")
    if not data or "username" not in data or "email" not in data or "password" not in data:
        return error_response("username、emailとpasswordは必須です", status=400)
    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], email=data["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return success_response("user登録しました")

@user_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return error_response("emailとpasswordは必須です", 400)
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return error_response("emailが登録されていません", status=404)
    if not check_password_hash(user.password, data["password"]):
        return error_response("パスワードが違います", 401)
    payload = {
        "user_id" : user.id,
        "exp" : datetime.datetime.now(ZoneInfo("Asia/Tokyo")) + datetime.timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    user_data = {"access_token": token}
    logger.info(f"{user.username}がログインしました")
    return success_response(user_data, "ログインしました", 200)

@user_bp.route("/logout", methods=['POST'])
def logout():
    session.clear()
    logger.info("ログアウトしました")
    return success_response("ログアウトしました", 200)

@user_bp.route("/check", methods=['GET'])
def check():
    if 'use_id' in session:
        return success_response("ログインしています", 200)
    return error_response("ログインしていません", 401)