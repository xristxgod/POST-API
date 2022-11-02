from typing import Type

from tortoise.contrib.pydantic import pydantic_model_creator

import src
from src.db.manager import Manager
from src.db.models import Comment


CommentBody = pydantic_model_creator(Comment, name="Post")


class CommentManager(Manager, metaclass=src.Singleton):
    model = Comment
    body = CommentBody


async def get_manager() -> Type[Manager]:
    return CommentManager


__all__ = [
    'CommentManager',
    'CommentBody',
    'get_manager'
]
