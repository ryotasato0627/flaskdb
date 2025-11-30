from flask import Blueprint, request
from ..services.auth import AuthService
from ..utils.response import error_response, success_response

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["post"])
def login():
    data = request.get_json()
    try:
        token = AuthService.login(data["email"], data["password"])
        return success_response(token, "ログイン完了", 200)
    except ValueError as e:
        return error_response(str(e), 400)