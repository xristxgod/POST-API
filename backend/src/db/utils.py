from typing import Dict

import pydantic
from tortoise import models


class MiddlewareUtils:
    @staticmethod
    async def middleware(body: pydantic.BaseModel, **fields: Dict[str: models.MODEL]) -> pydantic.BaseModel:
        # user=None - del body.user || post=Post - Post.get(id=post)
        for name, model in fields.items():
            if model is None:
                delattr(body, name)
            else:
                setattr(body, name, await model.get(id=getattr(body, name)))
        return body


__all__ = [
    'MiddlewareUtils'
]
