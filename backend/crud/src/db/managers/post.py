from typing import Type

from tortoise.contrib.pydantic import pydantic_model_creator

import src
from src.db.manager import Manager
from src.db.models import Post


PostBody = pydantic_model_creator(Post, name="Post")


class PostManager(Manager, metaclass=src.Singleton):
    model = Post
    response = PostBody


async def get_manager() -> Manager:
    return PostManager()


__all__ = [
    'PostManager',
    'PostBody',
    'get_manager'
]
