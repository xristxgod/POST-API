from typing import List

from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.transactions import in_transaction
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse

from src.db.models import User, PostImage
from src.db import Manager, get_post_manager
from src.db.managers.post import PostBody
from src.rest.schemas import ModPost, ResponseSuccessfully
from src.utils import CustomResponses


router = APIRouter()
image_router = APIRouter()


async def _user_middleware(body: PostBody, update: bool = False) -> PostBody:
    if update:
        del body.user
    else:
        body.user = await User.get(id=body.user)
    return body


@router.post('/', response_model=PostBody)
async def add_post(body: ModPost, db: Manager = Depends(get_post_manager)):
    return await db.add(body=await _user_middleware(body=body))


@router.get('/all', response_model=List[PostBody])
async def get_all_post(db: Manager = Depends(get_post_manager)):
    return await db.all()


@router.get('/{post_id}', response_model=PostBody, responses={404: {"model": HTTPNotFoundError}})
async def get_user(post_id: int, db: Manager = Depends(get_post_manager)):
    return await db.get(post_id)


@router.put('/{post_id}', response_model=ResponseSuccessfully, responses={404: {"model": HTTPNotFoundError}})
async def update_user(body: ModPost, post_id: int, db: Manager = Depends(get_post_manager)):
    await db.update(post_id, body=await _user_middleware(body=body, update=True))
    return ResponseSuccessfully()


@router.delete('/{post_id}', response_model=ResponseSuccessfully, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(post_id: int, db: Manager = Depends(get_post_manager)):
    await db.delete(post_id)
    return ResponseSuccessfully()


@image_router.patch(
    '/{post_id}/images', response_model=ResponseSuccessfully, responses={404: {"model": HTTPNotFoundError}}
)
async def add_images(post_id: int, images: List[UploadFile] = File(default=None)):
    async with in_transaction():
        await PostImage.create(main=True, image=images[0], post=post_id)
        if len(images) > 1:
            for image in images[1:]:
                await PostImage.create(
                    image=image,
                    post=post_id
                )
    return ResponseSuccessfully()


@image_router.get(
    '/{post_id}/images', response_class=StreamingResponse,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_all_images(post_id: int):
    images = await PostImage.filter(post=post_id).all()
    return CustomResponses.image_response([image.image for image in images])


@image_router.get(
    '/{post_id}/images/{image_id}?main={main}', response_class=StreamingResponse,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_image(post_id: int, image_id: int, main: bool = False):
    image = await PostImage.filter(id=image_id, post=post_id, main=main).first()
    return CustomResponses.image_response(image.image)


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
