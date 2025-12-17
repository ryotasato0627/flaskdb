from flask import session
from ..database import db
from ..models.note import Note

class NoteRepository:
    def get_all_notes(self):
        return Note.query.all()
    
    def get_note_by_id(self, note_id):
        note = Note.query.filter_by(id=note_id).first()
        if not note:
            raise ValueError("Noteが存在しません")
        return note

    def create_note(self, title, content, user_id):
        new_note = Note(title=title, content=content, user_id=user_id)
        db.session.add(new_note)
        return new_note
    
    def update_note(self, note_id, title, content):
        update_note = self.get_note_by_id(note_id)
        update_note.title = title
        update_note.content = content
        return update_note
    
    def delete_note(self, note_id):
        delete_note = self.get_note_by_id(note_id)
        db.session.delete(delete_note)
        return True