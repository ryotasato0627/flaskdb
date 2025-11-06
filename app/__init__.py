from flask import Flask
from app.database import db
from app.models.note import Note
from app.models.user import User
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from .routes.note import main_bp
    from .routes.user import user_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)


    return app