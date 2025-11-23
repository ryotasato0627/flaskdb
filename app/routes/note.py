from flask import Blueprint, session, request
from ..models.note import Note
from ..models.user import User
from app.database import db
from app.utils.response import success_response, error_response
from app.utils.logger import logger

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def root():
    return success_response(message="hello flask")

@main_bp.route("/notes", methods=["GET"])
def get_all_notes():
    notes = Note.query.all()
    user_id = session.get("user_id")
    if not user_id:
        return error_response("ログインしてください", 401)
    data = [note.to_dict() for note in notes]
    logger.info("Note一覧取得リクエストを受け取りました")
    return success_response(data, "Note一覧を取得しました")

@main_bp.route("/note/<int:id>", methods=["GET"])
def note_get_by_id(id):
    note = Note.query.get_or_404(id)
    logger.info(f"{id}のNoteの取得リクエストを受け取りました")
    return success_response(note.to_dict(), "Noteを取得しました")


@main_bp.route("/note", methods=["POST"])
def create_note():
    data = request.get_json()
    user_id = session.get("user_id")
    if not user_id:
        return error_response("ログインしてください", 401)
    if not data or "title" not in data or "content" not in data:
        return error_response("titleとcontentは必須です", 400)
    new_note = Note(title=data["title"], content=data["content"], user_id=user_id)
    db.session.add(new_note)
    db.session.commit()
    logger.info("Noteを作成しました")
    return success_response("Noteを作成しました")
    
@main_bp.route("/notes/<int:id>", methods=["PUT"])
def update_note(id):
    note = Note.query.get_or_404(id)
    data = request.get_json()
    user_id = session.get("user_id")
    if not user_id:
        return error_response("ログインしてください", 401)
    if not data or not "title" in data or not "content" in data:
        return error_response("titleとcontentは必須です", 400)
    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)
    db.session.commit()
    logger.info(f"{id}のNoteを更新しました")
    return success_response(note.to_dict(), "Noteを更新しました")

@main_bp.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    user_id = session.get("user_id")
    if not user_id:
        error_response("ログインしてください", 401)
    db.session.delete(note)
    db.session.commit()
    logger.info(f"{id}のNoteを削除しました")
    return success_response("Noteを削除しました")