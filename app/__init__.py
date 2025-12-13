from flask import Flask
from app.database import db
#from app.extensions import ma
from app.models.note import Note
from app.models.user import User
from .config import Config
from .utils.response import error_response
from .utils.logger import logger
import traceback
import jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    #ma.init_app(app)

    from .routes.note import main_bp
    from .routes.user import user_bp
    from .routes.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    @app.errorhandler(Exception)
    def handle_exception(e):
        db.session.rollback()
        error_trace = traceback.format_exc()
        logger.error(f"例外発生: {e}\n{error_trace}")
        return error_response("サーバー側でエラーが発生しました", 500)

    return app