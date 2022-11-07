from fastapi import APIRouter

from .user import router as user_router

from .post import router as post_router

from .comment import router as comment_router

from .image import router as image_router


api = APIRouter()

api.include_router(user_router, prefix='/users', tags=['USER'])

api.include_router(post_router, prefix='/posts', tags=['POST'])

api.include_router(comment_router, prefix='/comment', tags=['COMMENT'])

api.include_router(image_router, prefix='/images', tags=['IMAGE'])


__all__ = [
    'api'
]
