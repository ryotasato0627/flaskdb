from flask import Blueprint, request
from pydantic import ValidationError
from ..services.note import NoteService
from ..schemas.note import NoteCreateSchema, NoteUpdateSchema, NoteResponseSchema
from ..utils.response import success_response, error_response
from ..utils.token_required import token_required
from ..config import Config

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
@token_required
def root():
    return success_response(message="hello flask")

@main_bp.route("/notes", methods=["GET"])
@token_required
def get_all_notes(user_id):
    try:
        notes = NoteService.get_all_notes(user_id)
        return success_response([note.to_dict() for note in notes], "Note一覧を取得しました")
    except ValueError as e:
        return error_response(str(e), 404)


@main_bp.route("/note/<int:id>", methods=["GET"])
@token_required
def note_get_by_id(user_id, id):
    try:
        note = NoteService.get_note_by_id(id)
        return success_response(note.to_dict(), "Noteを取得しました")
    except ValueError as e:
        return error_response(str(e), 404)

@main_bp.route("/note", methods=["POST"])
@token_required
def create_note(user_id):
    try:
        data = NoteCreateSchema(**request.json)
        new_note = NoteService.create_note(user_id, data.title, data.content)
        response_schema = NoteResponseSchema.from_orm(new_note)
    except ValueError as e:
        return error_response(str(e), 404)
    except ValidationError as e:
        return error_response(str(e), 400)
    return success_response(response_schema.dict(), "Noteを作成しました", 200)

@main_bp.route("/note/<int:id>", methods=["PUT"])
@token_required
def update_note(user_id, id):
    try:
        data = NoteUpdateSchema(**request.json)
        update_note = NoteService.update_note(id,user_id, data.title, data.content)
        response_update_schema = NoteResponseSchema(**update_note)
    except ValueError as e:
        return error_response(str(e), 404)
    except ValidationError as e:
        return error_response(str(e), 400)
    return success_response(response_update_schema.dict(), "Noteを更新しました", 200)

@main_bp.route("/note/<int:id>", methods=["DELETE"])
@token_required
def delete_note(user_id, id):
    try:
        NoteService.delete_note(id, user_id)
        return success_response("Noteを削除しました")
    except ValueError as e:
        return error_response(str(e), 404)