from functools import wraps
from functools import requests
import jwt
from ..config import Config
from ..utils.response import error_response
from ..utils.token import TokenUtils

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header =requests.headers.get("Authorization")

        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return error_response("トークンが必要です", 401)
        
        try:
            payload = TokenUtils.decode_token(token)
            user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            return error_response("トークンの有効期限が切れています", 401)
        except jwt.InvalidTokenError:
            return error_response("無効なトークンです", 401)
        
        return f(user_id, *args, **kwargs)
    return decorated