from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi import APIRouter, Depends

from src.db import Manager, get_comment_manager
from src.db.managers.comment import CommentBody
from src.rest.schemas import ModComment, ResponseSuccessfully


router = APIRouter()


@router.post('/', response_model=CommentBody)
async def add_comment(body: ModComment, db: Manager = Depends(get_comment_manager)):
    return await db.add(body=body)


@router.get(
    '/{comment_id}', response_model=CommentBody,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_comment(comment_id: int, db: Manager = Depends(get_comment_manager)):
    return await db.get(comment_id)


@router.put('/{comment_id}', response_model=CommentBody, responses={404: {"model": HTTPNotFoundError}})
async def update_comment(body: ModComment, comment_id: int, db: Manager = Depends(get_comment_manager)):
    return await db.update(comment_id, body=body)


@router.delete('/{comment_id}', response_model=ResponseSuccessfully, responses={404: {"model": HTTPNotFoundError}})
async def delete_comment(comment_id: int, db: Manager = Depends(get_comment_manager)):
    await db.delete(comment_id)
    return ResponseSuccessfully()
