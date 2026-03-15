from app.database import db

class NoteTag(db.Model):
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)

    def to_dict(self):
        return {
            "note_id" : self.note_id,
            "tag_id" : self.tag_id
        }