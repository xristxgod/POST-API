from typing import List

from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi import APIRouter, Depends

from src.db.models import User
from src.db.utils import DatabaseMiddlewares
from src.db import Manager, get_post_manager
from src.db.managers.post import PostBody
from src.rest.schemas import ModPost, ResponseSuccessfully


router = APIRouter()


@router.post('/', response_model=PostBody)
async def add_post(body: ModPost, db: Manager = Depends(get_post_manager)):
    return await db.add(body=await DatabaseMiddlewares.name_middleware(body=body, user=User))


@router.get('/all', response_model=List[PostBody])
async def get_all_post(db: Manager = Depends(get_post_manager)):
    return await db.all()


@router.get('/{post_id}', response_model=PostBody, responses={404: {"model": HTTPNotFoundError}})
async def get_post(post_id: int, db: Manager = Depends(get_post_manager)):
    return await db.get(post_id)


@router.put('/{post_id}', response_model=ResponseSuccessfully, responses={404: {"model": HTTPNotFoundError}})
async def update_post(body: ModPost, post_id: int, db: Manager = Depends(get_post_manager)):
    await db.update(post_id, body=await DatabaseMiddlewares.name_middleware(body=body, user=None))
    return ResponseSuccessfully()


@router.delete('/{post_id}', response_model=ResponseSuccessfully, responses={404: {"model": HTTPNotFoundError}})
async def delete_post(post_id: int, db: Manager = Depends(get_post_manager)):
    await db.delete(post_id)
    return ResponseSuccessfully()


__all__ = [
    'router'
]
