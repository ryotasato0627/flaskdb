from sqlalchemy.orm import selectinload

from ..database import db
from ..models.note import Note
from ..models.tag import Tag


class NoteRepository:
    def get_all_notes(self, user_id, tag_id=None):
        try:
            query = Note.query.filter_by(user_id=user_id).options(selectinload(Note.tags))
            if tag_id is not None:
                query = query.join(Note.tags).filter(Tag.id == tag_id).distinct()
            return query.all()
        except Exception as e:
            db.session.rollback()
            raise

    def get_note_by_id(self, note_id):
        try:
            note = (
                Note.query.options(selectinload(Note.tags))
                .filter_by(id=note_id)
                .first()
            )
            if not note:
                raise ValueError("Noteが存在しません")
            return note
        except ValueError:
            raise
        except Exception as e:
            db.session.rollback()
            raise

    def create_note(self, title, content, user_id, tag_ids=None):
        try:
            new_note = Note(title=title, content=content, user_id=user_id)
            db.session.add(new_note)
            db.session.flush()
            if tag_ids:
                tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
                new_note.tags = tags
            db.session.commit()
            return new_note
        except Exception as e:
            db.session.rollback()
            raise

    def update_note(self, note_id, title=None, content=None, tag_ids=None):
        try:
            update_note = self.get_note_by_id(note_id)
            if title is not None:
                update_note.title = title
            if content is not None:
                update_note.content = content
            if tag_ids is not None:
                update_note.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            db.session.commit()
            return update_note
        except Exception as e:
            db.session.rollback()
            raise

    def delete_note(self, note_id, user_id):
        try:
            delete_note = self.get_note_by_id(note_id)
            db.session.delete(delete_note)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise