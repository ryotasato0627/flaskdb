from flask import session
from ..database import db
from ..models.note import Note

class NoteRepository:
    def get_all_notes(self):
        try:
            return Note.query.all()
        except Exception as e:
            db.session.rollback()
            raise

    def get_note_by_id(self, note_id):
        try:
            note = Note.query.filter_by(id=note_id).first()
            if not note:
                raise ValueError("Noteが存在しません")
            return note
        except Exception as e:
            db.session.rollback()
            raise

    def create_note(self, title, content, user_id):
        try:
            new_note = Note(title=title, content=content, user_id=user_id)
            db.session.add(new_note)
            db.session.commit()
            return new_note
        except Exception as e:
            db.session.rollback()
            raise

    def update_note(self, note_id, title, content):
        try:
            update_note = self.get_note_by_id(note_id)
            update_note.title = title
            update_note.content = content
            db.session.commit()
            return update_note
        except Exception as e:
            db.session.rollback()
            raise

    def delete_note(self, note_id):
        try:
            delete_note = self.get_note_by_id(note_id)
            db.session.delete(delete_note)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise