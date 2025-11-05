from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.user import User
from app.database import db
from app.utils.response import success_response, erorr_resoponse

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    if not data or "username" not in data or "email" not in data or "password" not in data:
        return erorr_resoponse("username、emailとpasswordは必須です", status=400)
    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], email=data["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return success_response("user登録しました")

@user_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    if not data or "email" in data or "password" in data:
        return erorr_resoponse("emailとpasswordは必須です", status=400)
    user = user.query.filter_by(email=data["email"]).first()
    if not user:
        return erorr_resoponse("emailが登録されていません", status=404)
    if not check_password_hash(user.password_hash, data["password"]):
        return erorr_resoponse("パスワードが違います", status=401)
    session['user_id'] = user.id
    session['user_email'] = user.email
    session["username"] = user.username

    return success_response("ログインしました", status=200)

@user_bp.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return success_response("ログアウトしました", status=200)

@user_bp.route("/check", methods=['GET'])
def check():
    if 'use_id' in session:
        return success_response("ログインしています", status=200)
    return erorr_resoponse("ログインしていません", status=401)