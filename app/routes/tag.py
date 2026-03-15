from flask import Blueprint, request
from pydantic import ValidationError

from ..schemas.tag import TagCreateSchema, TagSchema
from ..services.tag import TagService
from ..utils.response import success_response, error_response
from ..utils.token_required import token_required

tag_bp = Blueprint("tag", __name__)
tag_service = TagService()


@tag_bp.route("/tags", methods=["GET"])
@token_required
def get_all_tags(user_id):
    try:
        tags = tag_service.get_all_tags()
        return success_response(
            [TagSchema.from_orm(t).dict() for t in tags],
            "タグ一覧を取得しました",
        )
    except Exception as e:
        return error_response(str(e), 500)


@tag_bp.route("/tags", methods=["POST"])
@token_required
def create_tag(user_id):
    try:
        data = TagCreateSchema(**request.json)
        tag = tag_service.create_tag(data.name)
        return success_response(
            TagSchema.from_orm(tag).dict(),
            "タグを作成しました",
            201,
        )
    except ValueError as e:
        return error_response(str(e), 400)
    except ValidationError as e:
        return error_response(str(e), 400)
