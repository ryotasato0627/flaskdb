from datetime import datetime
from zoneinfo import ZoneInfo
from app.database import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(ZoneInfo("Asia/Tokyo")))

    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "content" : self.content,
            "created_at" : self.created_at
        }