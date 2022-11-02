from typing import List

from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse

from src.db.models import User
from src.db import Manager, get_user_manager
from src.db.managers.user import UserBody
from src.rest.schemas import ModUser, ResponseSuccessfully
from src.utils import CustomResponses


router = APIRouter()
avatar_router = APIRouter()


@router.post('/', response_model=UserBody)
async def add_user(body: ModUser, db: Manager = Depends(get_user_manager)):
    return await db.add(body=body)


@router.get('/all', response_model=List[UserBody])
async def get_all_users(db: Manager = Depends(get_user_manager)):
    return await db.all()


@router.get(
    '/{user_id}', response_model=UserBody,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int, db: Manager = Depends(get_user_manager)):
    return await db.get(user_id)


@router.put('/{user_id}', response_model=UserBody, responses={404: {"model": HTTPNotFoundError}})
async def update_user(body: ModUser, user_id: int, db: Manager = Depends(get_user_manager)):
    return await db.update(user_id, body=body)


@router.delete('/{user_id}', response_model=ResponseSuccessfully, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int, db: Manager = Depends(get_user_manager)):
    await db.delete(user_id)
    return ResponseSuccessfully()


@avatar_router.put(
    '/{user_id}/avatar', response_model=ResponseSuccessfully,
    responses={404: {"model": HTTPNotFoundError}}
)
async def add_avatar(user_id: int, avatar: UploadFile = File(default=None)):
    user = await User.get(id=user_id)
    await user.update_from_dict({'avatar': await avatar.read()}).save()
    return ResponseSuccessfully()


@avatar_router.delete(
    '/{user_id}/avatar', response_model=ResponseSuccessfully,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_avatar(user_id: int):
    user = await User.get(id=user_id)
    await user.update_from_dict({'avatar': None}).save()
    return ResponseSuccessfully()


@avatar_router.get(
    '/{user_id}/avatar', response_class=StreamingResponse,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_avatar(user_id: int):
    user = await User.filter(id=user_id).first()
    return CustomResponses.image_response(user.avatar)


__all__ = [
    'router', 'avatar_router'
]
