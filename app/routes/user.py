from flask import Blueprint, request
from pydantic import ValidationError
from ..services.user import UserService
from ..schemas.user import UserSchema
from app.utils.response import success_response, error_response

user_bp = Blueprint('user', __name__, url_prefix="/user")

@user_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = UserSchema(**request.json)
        UserService.register(data.username, data.email, data.password)
    except ValidationError as e:
        return error_response(str(e), 400)
    except ValueError as e:
        return error_response(str(e), 400)
    return success_response("user登録しました", 200)