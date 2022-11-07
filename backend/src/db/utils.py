import enum

import pydantic
import tortoise.models as models
from tortoise.validators import Validator, ValidationError
from fastapi import HTTPException, status


class ImageTypeEnum(enum.Enum):
    post = 'post'
    user = 'user'
    comment = 'comment'


class DatabaseMiddlewares:
    @staticmethod
    async def name_middleware(body: pydantic.BaseModel, **fields) -> pydantic.BaseModel:
        # user=None - del body.user || post=Post - Post.get(id=post)
        for name, model in fields.items():
            model: models.MODEL
            if model is None:
                delattr(body, name)
            else:
                setattr(body, name, await model.get(id=getattr(body, name)))
        return body


class DatabaseValidators:

    @staticmethod
    async def itme_validator(item_type: ImageTypeEnum, item_id: int):
        import src.db.models as m

        item_obj_name: str = item_type.name.title()
        item_obj: models.MODEL = getattr(m, item_obj_name, None)

        if await item_obj.get_or_none(id=item_id) is None:
            raise HTTPException(
                detail=f'There is no element with the value {item_id} in the {item_obj_name} model.',
                status_code=status.HTTP_400_BAD_REQUEST
            )


__all__ = [
    'DatabaseMiddlewares',
    'DatabaseValidators',
    'ImageTypeEnum'
]
