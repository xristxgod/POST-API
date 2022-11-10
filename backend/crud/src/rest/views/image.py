import io
import enum
from typing import List

from tortoise.models import MODEL
from tortoise.transactions import in_transaction
from fastapi import APIRouter, Query, UploadFile, File, HTTPException, status
from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi.responses import StreamingResponse

import src.db.models as models
from src.rest.schemas import ResponseSuccessfully
from src.utils import Default


class ImageTypeEnum(enum.Enum):
    post = 'post'
    user = 'user'
    comment = 'comment'


class ImageController:
    model: MODEL = models.Image

    @staticmethod
    def check_count(count: int):
        if count == 5:
            raise HTTPException(detail='Too many image in database', status_code=status.HTTP_200_OK)

    @classmethod
    async def add(cls, item_type: ImageTypeEnum, item_id: int, images: List[UploadFile]) -> ResponseSuccessfully:
        params = {item_type.value: item_id}
        print(params)
        list_images = await cls.model.filter(**params)
        # To many image in database
        count_images = len(list_images)
        cls.check_count(count_images)
        async with in_transaction():
            if len(list_images) == 0:
                # Set main photo
                main_image = images.pop()
                print(params)
                await cls.model.create(image=await main_image.read(), main=True, **params)
            for image in images:
                await cls.model.create(image=await image.read(), **params)
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
    async def update(cls, image_id: int, item_type: ImageTypeEnum) -> ResponseSuccessfully:
        async with in_transaction():
            image = await cls.model.get(id=image_id)
            if not image.main:
                main_image = await cls.model.filter(
                    main=True, **{item_type: getattr(image, item_type.value)}
                ).first()

                main_image.main = False
                image.main = True

                await main_image.save()
                await image.save()
        return ResponseSuccessfully()

    @classmethod
    async def delete(cls, image_ids: List[int], item_type: ImageTypeEnum) -> ResponseSuccessfully:
        change_params = None
        async with in_transaction():
            for image_id in image_ids:
                image = await cls.model.get(id=image_id)
                if image.main:
                    change_params = {item_type: getattr(image, item_type.value)}
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
async def add_images(item_type: ImageTypeEnum, item_id: int, images: List[UploadFile] = File(default=None)):
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
    '/{item_type}/update-main-image/{image_id}', response_model=ResponseSuccessfully,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_main_image(item_type: ImageTypeEnum, image_id: int):
    return await ImageController.update(image_id=image_id, item_type=item_type)


@router.delete(
    '/', response_model=ResponseSuccessfully,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_images(image_ids: List[int] = Query()):
    return await ImageController.delete(image_ids=image_ids)


__all__ = [
    'router'
]
