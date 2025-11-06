from datetime import datetime
from zoneinfo import ZoneInfo
from app.database import db

class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(ZoneInfo("Asia/Tokyo")))

    def to_dict(self, inclube_password=False):
        data =  {
            "id" : self.id,
            "username" : self.username,
            "email" : self.email,
            "created_at" : self.created_at,
            "update_at" : self.update_at
        }
        if inclube_password:
            data["password"] = self.password
        return data
