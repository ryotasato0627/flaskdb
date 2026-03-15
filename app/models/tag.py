from app.database import db

# 中間テーブル（モデルクラスなし）。FK に CASCADE でノート削除時に紐づきのみ削除。
note_tag = db.Table(
    "note_tag",
    db.Column("note_id", db.Integer, db.ForeignKey("note.id", ondelete="CASCADE"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }