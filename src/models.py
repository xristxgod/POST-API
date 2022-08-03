from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, ForeignKey, orm
from sqlalchemy.types import Integer, VARCHAR, Text, DateTime

from src.base.schemas import (
    BodyCreateUser, ResponseUser,
    BodyCreateComment,
    BodyCreatePost
)
from .base import CRUD
from config import Config, logger


BaseModel = orm.declarative_base()
engine = sqlalchemy.create_engine(Config.DATABASE_URL)
session = orm.Session(engine)


class UserModel(BaseModel, CRUD):
    """User model"""
    __tablename__ = "user_model"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    username = Column(VARCHAR(50), unique=True)
    password = Column(VARCHAR(50))
    first_name = Column(VARCHAR(50), nullable=True)
    last_name = Column(VARCHAR(50), nullable=True)

    def __repr__(self):
        return f"{self.username}"

    @staticmethod
    def create(data: BodyCreateUser) -> bool:
        """Create new user"""
        try:
            session.add(UserModel(
                username=data.username,
                password=data.password,
                first_name=data.firstName,
                last_name=data.lastName
            ))
            session.commit()
            return True
        except Exception as error:
            logger.error(f"{error}")
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def read(user_id: int) -> ResponseUser:
        try:
            user: UserModel = session.query(UserModel).get(user_id)
            if not user:
                raise NotImplementedError
            return ResponseUser(
                username=user.username,
                password=user.password,
                firstName=user.first_name,
                lastName=user.last_name,
            )
        except NotImplementedError as error:
            raise ValueError("This user does not exist in the system.")
        except Exception as error:
            logger.error(f"{error}")
            raise ValueError("Is there something wrong!")
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

    authors = orm.relationship("UserModel", foreign_keys="PostModel.author_id")

    @staticmethod
    def create(data: BodyCreatePost) -> bool:
        """Create new post"""
        try:
            session.add(PostModel(
                title=data.title,
                text=data.text,
                author_id=data.authorId,
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

    parents = orm.relationship("UserModel", foreign_keys="CommentModel.parent_id")
    authors = orm.relationship("UserModel", foreign_keys="CommentModel.author_id")
    posts = orm.relationship('PostModel', foreign_keys="CommentModel.post_id")

    @staticmethod
    def create(data: BodyCreateComment) -> bool:
        """Create new comment"""
        try:
            session.add(CommentModel(
                text=data.text,
                parent_id=data.parentId,
                post_id=data.postId,
                author_id=data.authorId,
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
