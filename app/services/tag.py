from sqlalchemy.exc import IntegrityError

from ..repository.tag import TagRepository
from ..utils.logger import logger


class TagService:
    def __init__(self, tag_repo: TagRepository = None):
        self.tag_repo = tag_repo or TagRepository()

    def get_all_tags(self):
        tags = self.tag_repo.get_all()
        logger.info("タグ一覧を取得しました")
        return tags

    def create_tag(self, name):
        if not name or not name.strip():
            raise ValueError("タグ名は必須です")
        existing = self.tag_repo.get_by_name(name.strip())
        if existing:
            raise ValueError("同名のタグが既に存在します")
        try:
            tag = self.tag_repo.create(name.strip())
            logger.info(f"タグを作成しました: {tag.name}")
            return tag
        except IntegrityError:
            raise ValueError("同名のタグが既に存在します")
