from fastapi import APIRouter

from .user import router as user_router
from .user import avatar_router

from .post import router as post_router
from .post import image_router

from .comment import router as comment_router


api = APIRouter()

api.include_router(user_router, prefix='/users', tags=['USER'])
api.include_router(avatar_router, prefix='/users', tags=['USER-AVATAR'])

api.include_router(post_router, prefix='/posts', tags=['POST'])
api.include_router(image_router, prefix='/posts', tags=['POST-IMAGE'])

api.include_router(comment_router, prefix='/comment', tags=['COMMENT'])


# @api.get('/user/')
# async def get_all_posts_by_user_id():
#     pass





__all__ = [
    'api'
]
