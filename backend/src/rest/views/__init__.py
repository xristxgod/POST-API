from typing import Union

from fastapi import APIRouter, HTTPException, status

from .user import router as user_router

from .post import router as post_router

from .comment import router as comment_router

from .image import router as image_router

from src.rest.schemas import AuthenticationBody, ResponseMessage
from src.db import models
from src.db.managers import user as user_manager


api = APIRouter()

api.include_router(user_router, prefix='/users', tags=['USER'])

api.include_router(post_router, prefix='/posts', tags=['POST'])

api.include_router(comment_router, prefix='/comment', tags=['COMMENT'])

api.include_router(image_router, prefix='/images', tags=['IMAGE'])


@api.post(
    '/authentication',
    tags=['OPTIONS'],
    response_model=user_manager.UserBody
)
async def authentication(body: AuthenticationBody):
    user = await models.User.filter(username=body.username).first()
    if not user.verify_password(body.password):
        raise HTTPException(detail='Not authenticated', status_code=status.HTTP_401_UNAUTHORIZED)
    return await user_manager.UserBody.from_tortoise_orm(user)


__all__ = [
    'api'
]
