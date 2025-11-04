from flask import Blueprint, jsonify, request
from ..models.note import Note
from app.database import db
from app.utils.response import success_response, erorr_resoponse

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def root():
    return success_response(message="hello flask")

@main_bp.route("/notes", methods=["GET"])
def get_all_notes():
    try:
        notes = Note.query.all()
        data = [note.to_dict() for note in notes]
        return success_response(data, "Note一覧を取得しました")
    except Exception as e:
        return erorr_resoponse("Noteの一覧取得に失敗しました", e)
    
@main_bp.route("/note/<int:id>", methods=["GET"])
def note_get_by_id(id):
    try:
        note = Note.query.get_or_404(id)
        return success_response(note.to_dict(), "Noteを取得しました")
    except Exception as e:
        return erorr_resoponse("Noteの取得失敗しました", e)

@main_bp.route("/note", methods=["POST"])
def create_note():
    try:
        data = request.get_json()
        if not data or "title" not in data or "content" not in data:
            return erorr_resoponse("titleとcontentは必須です", status=400)
        new_note = Note(title=data["title"], content=data["content"])
        db.session.add(new_note)
        db.session.commit()
        return success_response("Noteを作成しました")
    except Exception as e:
        db.session.rollback()
        return erorr_resoponse("Noteの投稿に失敗しました", e)
    
@main_bp.route("/notes/<int:id>", methods=["PUT"])
def update_note(id):
    try:
        note = Note.query.get_or_404(id)
        data = request.get_json()
        if not data or not "title" in data or not "content" in data:
            return erorr_resoponse("titleとcontentは必須です", e)
        note.title = data.get("title", note.title)
        note.content = data.get("content", note.content)
        db.session.commit()
        return success_response(note.to_dict(), "Noteを更新しました")
    except Exception as e:
        return erorr_resoponse("Noteの更新に失敗しました", e)

@main_bp.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    try:
        note = Note.query.get_or_404(id)
        db.session.delete(note)
        db.session.commit()
        return success_response("Noteを削除しました")
    except Exception as e:
        return erorr_resoponse("削除に失敗しました", e)