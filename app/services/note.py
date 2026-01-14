from ..models.note import Note
from ..database import db
from ..repository.note import NoteRepository
from ..utils.logger import logger


class NoteService:
    def __init__(self, note_repo: NoteRepository):
        self.note_repo = note_repo

    def get_all_notes(self):
        notes = self.note_repo.get_all_notes()
        logger.info("全てのNoteを取得しました")
        return notes
    
    def get_note_by_id(self, note_id):
        note = self.note_repo.get_note_by_id(note_id)
        logger.info(f"Note ID {note_id} を取得しました")
        return note
    
    def create_note(self, user_id, title, content):
        if not title or not content:
            raise ValueError("titleとcontentは必須です")
        new_note = self.note_repo.create_note(title, content, user_id)
        logger.info(f"新しいNoteを作成しました: {title}")
        return new_note
    
    def update_note(self, user_id, note_id, title, content):
        if not title or not content:
            raise ValueError("titleとcontentは必須です")
        update_note = self.note_repo.get_note_by_id(note_id)
        NoteService.check_permission(update_note, user_id)
        update_note = self.note_repo.update_note(note_id, title, content)
        db.session.commit()
        logger.info(f"Note ID {note_id} を更新しました")
        return update_note
    
    def delete_note(self, note_id, user_id):
        NoteService.check_permission(self.note_repo.get_note_by_id(note_id), user_id)
        self.note_repo.delete_note(note_id, user_id)
        db.session.commit()
        logger.info(f"Note ID {note_id} を削除しました")
        return True
    
    @staticmethod
    def check_permission(note, user_id):
        if note.user_id != user_id:
            raise PermissionError("権限がありません")
