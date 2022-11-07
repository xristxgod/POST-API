import io
from typing import List

from tortoise.models import MODEL
from tortoise.transactions import in_transaction
from fastapi import APIRouter, Query, UploadFile, File, HTTPException, status
from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi.responses import StreamingResponse

import src.db.models as models
import src.db.utils as database_utils
from src.rest.schemas import ResponseSuccessfully
from src.utils import Default


class ImageController:
    model: MODEL = models.Image

    @staticmethod
    def check_count(count: int):
        if count == 5:
            raise HTTPException(detail='Too many image in database', status_code=status.HTTP_200_OK)

    @classmethod
    async def add(cls, item_type: models.ImageTypeEnum, item_id: int, images: List[UploadFile]) -> ResponseSuccessfully:
        list_images = cls.model.filter(type=item_type, item_id=item_id)
        # To many image in database
        count_images = len(list_images)
        cls.check_count(count_images)
        base_params = dict(type=item_type, item_id=item_id)
        async with in_transaction():
            if len(list_images) == 0:
                # Set main photo
                main_image = images.pop()
                await cls.model.create(main=True, image=await main_image.read(), **base_params)
            for image in images:
                await cls.model.create(image=await image.read(), **base_params)
                count_images += 1
                cls.check_count(count_images)
        return ResponseSuccessfully()

    @classmethod
    async def get(cls, image_id: int) -> StreamingResponse:
        image = await cls.model.get_or_none(id=image_id)
        return StreamingResponse(
            io.BytesIO(image.image) if image is not None else await Default.default_image(),
            media_type='image/png'
        )

    @classmethod
    async def update(cls, image_id: int) -> ResponseSuccessfully:
        image = await cls.model.get(id=image_id)
        if not image.main:
            async with in_transaction():
                main_image = await cls.model.filter(type=image.type, item_id=image.item_id, main=True).first()

                main_image.main = False
                image.main = True

                await main_image.save()
                await image.save()

        return ResponseSuccessfully()

    @classmethod
    async def delete(cls, image_ids: List[int]) -> ResponseSuccessfully:
        change_params = None
        async with in_transaction():
            for image_id in image_ids:
                image = await cls.model.get(id=image_id)
                if image.main:
                    change_params = dict(type=image.type, item_id=image.item_id)
                await image.delete()
                await image.save()

            if change_params is not None:
                images = await cls.model.filter(**change_params)
                if len(images) > 0:
                    new_main_image = await images.first()
                    new_main_image.main = True
                    new_main_image.save()
        return ResponseSuccessfully()


router = APIRouter()


@router.patch(
    '/{item_type}={item_id}', response_model=ResponseSuccessfully,
    responses={404: {"model": HTTPNotFoundError}}
)
async def add_images(item_type: models.ImageTypeEnum, item_id: int, images: List[UploadFile] = File(default=None)):
    await database_utils.DatabaseValidators.itme_validator(item_type=item_type, item_id=item_id)
    return await ImageController.add(
        item_type=item_type,
        item_id=item_id,
        images=images
    )


@router.get(
    '/{image_id}', response_class=StreamingResponse,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_image(image_id: int):
    return await ImageController.get(image_id=image_id)


@router.put(
    '/update-main-image/{image_id}', response_model=ResponseSuccessfully,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_main_image(image_id: int):
    return await ImageController.update(image_id=image_id)


@router.delete(
    '/', response_model=ResponseSuccessfully,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_images(image_ids: List[int] = Query()):
    return await ImageController.delete(image_ids=image_ids)


__all__ = [
    'router'
]
