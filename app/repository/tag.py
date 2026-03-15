from ..database import db
from ..models.tag import Tag


class TagRepository:
    def get_all(self):
        try:
            return Tag.query.order_by(Tag.name).all()
        except Exception as e:
            db.session.rollback()
            raise

    def get_by_id(self, tag_id):
        try:
            tag = Tag.query.filter_by(id=tag_id).first()
            if not tag:
                raise ValueError("Tagが存在しません")
            return tag
        except ValueError:
            raise
        except Exception as e:
            db.session.rollback()
            raise

    def get_by_name(self, name):
        try:
            return Tag.query.filter_by(name=name).first()
        except Exception as e:
            db.session.rollback()
            raise

    def create(self, name):
        try:
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()
            return tag
        except Exception as e:
            db.session.rollback()
            raise
