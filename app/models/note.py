from datetime import datetime
from zoneinfo import ZoneInfo
from app.database import db
from app.models.tag import note_tag

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(ZoneInfo("Asia/Tokyo")))
    updated_at = db.Column(db.DateTime, default=datetime.now(ZoneInfo("Asia/Tokyo")))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tags = db.relationship("Tag", secondary=note_tag, backref="notes", lazy="select")

    def to_dict(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "title" : self.title,
            "content" : self.content,
            "created_at" : self.created_at,
            "updated_at" : self.updated_at,
            "tags" : [tag.to_dict() for tag in self.tags]
        }