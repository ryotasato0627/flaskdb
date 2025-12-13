import jwt
from ..config import Config
import datetime
from zoneinfo import ZoneInfo

class TokenUtils:
    @staticmethod
    def decode_token(token):
        return jwt.decode(token, Config.SECRET_KEY, algorithms="HS256")
    
    @staticmethod
    def generate_token(user_id):
        payload = {
            "user_id" : user_id,
            "exp" : datetime.datetime.now(ZoneInfo("Asia/Tokyo")) + datetime.timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    
    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms = "HS256"
            )
            return payload
        
        except jwt.ExpiredSignatureError:
            raise ValueError("トークンの有効期限がきれています")
        
        except jwt.InvalidTokenError:
            raise ValueError("無効なトークンです")