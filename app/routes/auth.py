from flask import Blueprint, request
from pydantic import ValidationError
from ..services.auth import AuthService
from ..schemas.auth import AuthSchema
from ..utils.response import error_response, success_response

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["post"])
def login():
    try:
        data = AuthSchema(**request.json)
        token = AuthService.login(data.email, data.password)
    except ValidationError as e:
        error_response(str(e), 400)
    except ValueError as e:
        return error_response(str(e), 400)
    return success_response(token, "ログイン完了", 200)