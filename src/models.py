from datetime import datetime

import databases
import sqlalchemy
from sqlalchemy import Column, ForeignKey, orm
from sqlalchemy.types import Integer, VARCHAR, Text, DateTime

from config import Config


BaseModel = orm.declarative_base()
engine = sqlalchemy.create_engine(Config.DATABASE_URL)
session = orm.Session(engine)

database = databases.Database(Config.DATABASE_URL)


class UserModel(BaseModel):
    """User model"""
    __tablename__ = "user_model"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    username = Column(VARCHAR(50), unique=True)
    password = Column(VARCHAR(50))

    authors = orm.relationship("PostModel", backref="user", lazy=True)
    comments = orm.relationship("CommentModel", backref="user", lazy=True)


class PostModel(BaseModel):
    """Post model"""
    __tablename__ = "post_model"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(VARCHAR(50), default="Not title")
    text = Column(Text, default="Not text")
    create_at = Column(DateTime, default=datetime.now())
    author_id = Column(Integer, ForeignKey("user_model.id", ondelete="SET NULL"))

    posts = orm.relationship('CommentModel', backref='post', lazy=True)


class CommentModel(BaseModel):
    """Comments model"""
    __tablename__ = "comment_model"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    text = Column(Text, default="Not text")
    create_at = Column(DateTime, default=datetime.now())
    parent_id = Column(Integer, ForeignKey("user_model.id", ondelete="SET NULL"), default=None, nullable=True)
    post_id = Column(Integer, ForeignKey("post_model.id", ondelete="CASCADE"))
    author_id = Column(Integer, ForeignKey("user_model.id", ondelete="SET NULL"))


def create_db():
    """Create database and his tables"""
    BaseModel.metadata.create_all(engine)
