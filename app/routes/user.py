from flask import Blueprint, request
from ..models.user import User
from ..services.user import UserService
from app.utils.response import success_response, error_response
from ..utils.logger import logger

user_bp = Blueprint('user', __name__, url_prefix="/user")

@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    try:
        UserService.register(data["username"], data["email"], data["password"])
    except ValueError as e:
        return error_response(str(e), 400)
    return success_response("user登録しました", 200)

@user_bp.route("/logout", methods=['POST'])
def logout():
    logger.info("ログアウトしました")
    return success_response("ログアウトしました", 200)

@user_bp.route("/check", methods=['GET'])
def check():
    if 'use_id' in session:
        return success_response("ログインしています", 200)
    return error_response("ログインしていません", 401)