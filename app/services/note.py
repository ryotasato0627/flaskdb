from ..models.note import Note
from ..database import db
from ..repository.note import NoteRepository
from ..utils.logger import logger


class NoteService:
    note_repo = None  # クラス経由で呼ぶとき用。インスタンスでは __init__ で上書き

    def __init__(self, note_repo: NoteRepository = None):
        self.note_repo = note_repo or NoteRepository()

    def get_all_notes(self, user_id, tag_id=None):
        repo = self.note_repo if self.note_repo is not None else NoteRepository()
        notes = repo.get_all_notes(user_id, tag_id=tag_id)
        logger.info("ユーザーに紐づくNote一覧を取得しました")
        return notes

    def get_note_by_id(self, note_id):
        repo = self.note_repo if self.note_repo is not None else NoteRepository()
        note = repo.get_note_by_id(note_id)
        logger.info(f"Note ID {note_id} を取得しました")
        return note

    def create_note(self, user_id, title, content, tag_ids=None):
        if not title or not content:
            raise ValueError("titleとcontentは必須です")
        repo = self.note_repo if self.note_repo is not None else NoteRepository()
        new_note = repo.create_note(title, content, user_id, tag_ids=tag_ids)
        logger.info(f"新しいNoteを作成しました: {title}")
        return new_note

    def update_note(self, user_id, note_id, title=None, content=None, tag_ids=None):
        if title is not None and (not title or not str(title).strip()):
            raise ValueError("titleとcontentは必須です")
        if content is not None and not str(content):
            raise ValueError("titleとcontentは必須です")
        repo = self.note_repo if self.note_repo is not None else NoteRepository()
        existing_note = repo.get_note_by_id(note_id)
        self.check_permission(existing_note, user_id)
        updated_note = repo.update_note(note_id, title, content, tag_ids=tag_ids)
        logger.info(f"Note ID {note_id} を更新しました")
        return updated_note

    def delete_note(self, note_id, user_id):
        repo = self.note_repo if self.note_repo is not None else NoteRepository()
        NoteService.check_permission(repo.get_note_by_id(note_id), user_id)
        repo.delete_note(note_id, user_id)
        logger.info(f"Note ID {note_id} を削除しました")
        return True

    @staticmethod
    def check_permission(note, user_id):
        if note.user_id != user_id:
            raise PermissionError("権限がありません")
