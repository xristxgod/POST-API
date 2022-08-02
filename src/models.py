from datetime import datetime

import databases
import sqlalchemy
from sqlalchemy import Column, ForeignKey, orm
from sqlalchemy.types import Integer, VARCHAR, Text, DateTime

from .schemas import BodyUser, BodyPost, BodyComment
from .base import CRUD
from config import Config, logger


BaseModel = orm.declarative_base()
engine = sqlalchemy.create_engine(Config.DATABASE_URL)
session = orm.Session(engine)

database = databases.Database(Config.DATABASE_URL)


class UserModel(BaseModel, CRUD):
    """User model"""
    __tablename__ = "user_model"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    username = Column(VARCHAR(50), unique=True)
    password = Column(VARCHAR(50))
    first_name = Column(VARCHAR(50), nullable=True)
    last_name = Column(VARCHAR(50), nullable=True)

    authors = orm.relationship("PostModel", backref="user", lazy=True)
    comments = orm.relationship("CommentModel", backref="user", lazy=True)

    @staticmethod
    def create(data: BodyUser) -> bool:
        """Create new user"""
        try:
            session.add(UserModel(
                username=data.username,
                password=data.password,
                first_name=data.firstName,
                last_name=data.lastName
            ))
            session.commit()
        except Exception as error:
            logger.error(f"{error}")
            session.rollback()
            return False
        finally:
            session.close()


class PostModel(BaseModel, CRUD):
    """Post model"""
    __tablename__ = "post_model"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(VARCHAR(50), default="Not title")
    text = Column(Text, default="Not text")
    create_at = Column(DateTime, default=datetime.now(), nullable=True)
    update_at = Column(DateTime, default=datetime.now(), nullable=True)
    author_id = Column(Integer, ForeignKey("user_model.id", ondelete="SET NULL"))

    posts = orm.relationship('CommentModel', backref='post', lazy=True)

    @staticmethod
    def create(data: BodyPost) -> bool:
        """Create new post"""
        try:
            session.add(PostModel(
                title=data.title,
                text=data.text,
                author_id=data.authorId
            ))
            session.commit()
        except Exception as error:
            logger.error(f"{error}")
            session.rollback()
            return False
        finally:
            session.close()


class CommentModel(BaseModel, CRUD):
    """Comments model"""
    __tablename__ = "comment_model"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    text = Column(Text, default="Not text")
    create_at = Column(DateTime, default=datetime.now(), nullable=True)
    update_at = Column(DateTime, default=datetime.now(), nullable=True)
    parent_id = Column(Integer, ForeignKey("user_model.id", ondelete="SET NULL"), default=None, nullable=True)
    post_id = Column(Integer, ForeignKey("post_model.id", ondelete="CASCADE"))
    author_id = Column(Integer, ForeignKey("user_model.id", ondelete="SET NULL"))

    @staticmethod
    def create(data: BodyComment) -> bool:
        """Create new comment"""
        try:
            session.add(CommentModel(
                text=data.text,
                parent_id=data.parentId,
                post_id=data.postId,
                author_id=data.authorId
            ))
            session.commit()
        except Exception as error:
            logger.error(f"{error}")
            session.rollback()
            return False
        finally:
            session.close()


def create_db():
    """Create database and his tables"""
    BaseModel.metadata.create_all(engine)
