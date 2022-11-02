from .models import User

from src.db.managers import post


class MiddlewareUtils:
    @staticmethod
    async def user_middleware(body: post.PostBody, update: bool = False) -> post.PostBody:
        if update:
            del body.user
        else:
            body.user = await User.get(id=body.user)
        return body
