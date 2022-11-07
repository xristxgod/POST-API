import os
import io
from typing import List

import aiofiles
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.transactions import in_transaction
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse

import src.settings as settings
from src.db.models import PostImage, User
from src.db.utils import MiddlewareUtils
from src.db import Manager, get_post_manager
from src.db.managers.post import PostBody
from src.rest.schemas import ModPost, ResponseSuccessfully
from src.utils import Default


router = APIRouter()
image_router = APIRouter()


@router.post('/', response_model=PostBody)
async def add_post(body: ModPost, db: Manager = Depends(get_post_manager)):
    return await db.add(body=await MiddlewareUtils.middleware(body=body, user=User))


@router.get('/all', response_model=List[PostBody])
async def get_all_post(db: Manager = Depends(get_post_manager)):
    return await db.all()


@router.get('/{post_id}', response_model=PostBody, responses={404: {"model": HTTPNotFoundError}})
async def get_post(post_id: int, db: Manager = Depends(get_post_manager)):
    return await db.get(post_id)


@router.put('/{post_id}', response_model=ResponseSuccessfully, responses={404: {"model": HTTPNotFoundError}})
async def update_post(body: ModPost, post_id: int, db: Manager = Depends(get_post_manager)):
    await db.update(post_id, body=await MiddlewareUtils.middleware(body=body, user=None))
    return ResponseSuccessfully()


@router.delete('/{post_id}', response_model=ResponseSuccessfully, responses={404: {"model": HTTPNotFoundError}})
async def delete_post(post_id: int, db: Manager = Depends(get_post_manager)):
    await db.delete(post_id)
    return ResponseSuccessfully()


# <<<================================================================================================================>>>


@image_router.patch(
    '/{post_id}/images', response_model=ResponseSuccessfully, responses={404: {"model": HTTPNotFoundError}}
)
async def add_images(post_id: int, images: List[UploadFile] = File(default=None)):
    async with in_transaction():
        # first photo is a main
        await PostImage.create(main=True, image=await images.pop().read())
        if len(images) > 0:
            for image in images:
                await PostImage.create(image=image, post=post_id)
    return ResponseSuccessfully()


@image_router.get(
    '/{post_id}/images/all', response_class=StreamingResponse,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_all_images(post_id: int):
    # images = await PostImage.filter(post=post_id).all()
    pass


@image_router.get(
    '/{post_id}/images/main', response_class=StreamingResponse,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_main_photo(post_id: int):
    image = await PostImage.filter(post=post_id, main=True).first()
    return StreamingResponse(
        io.BytesIO(image.image) if image.image is not None else Default.default_image(),
        media_type='image/png'
    )


@image_router.delete(
    '/{post_id}/images/{image_id}', response_model=ResponseSuccessfully,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_image(post_id: int, image_id: int):
    async with in_transaction():
        image = await PostImage.filter(id=image_id, post=post_id).first()
        if image.main:
            post = await PostImage.filter(post=post_id, main=False).first()
            post.main = True
        await image.delete()
        await image.save()
    return ResponseSuccessfully()


__all__ = [
    'router', 'image_router'
]
