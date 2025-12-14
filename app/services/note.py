from flask import Flask
from ..models.note import Note
from ..database import db
from ..utils.logger import logger

class NoteService:
    @staticmethod
    def get_all_notes():
        notes = Note.query.all()
        logger.info("全てのNoteを取得しました")
        return notes
    
    @staticmethod
    def get_note_by_id(note_id):
        note = Note.query.get(note_id)
        if not note:
            raise ValueError("Noteが存在しません")
        logger.info(f"Note ID {note_id} を取得しました")
        return note
    
    @staticmethod
    def create_note(user_id, title, content):
        if not title or not content:
            raise ValueError("titleとcontentは必須です")
        new_note = Note(title=title, content=content, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()
        logger.info(f"新しいNoteを作成しました: {title}")
        return new_note
    
    @staticmethod
    def update_note(note_id, user_id, title, content):
        update_note = Note.query.get(note_id)
        if update_note.user_id != user_id:
            raise ValueError("編集できるのは自分が作成したNoteのみです")
        if not title or not content:
            raise ValueError("titleとcontentは必須です")
        update_note.title = title
        update_note.content = content
        db.session.commit()
        logger.info(f"Note ID {note_id} を更新しました")
        return update_note
    
    @staticmethod
    def delete_note(note_id, user_id):
        delete_note = Note.query.get(note_id)
        if delete_note.user_id != user_id:
            raise ValueError("削除できるのは自分が作成したNoteのみです")
        db.session.delete(delete_note)
        db.session.commit()
        logger.info(f"Note ID {note_id} を削除しました")
        return True