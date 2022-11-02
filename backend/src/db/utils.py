import pydantic
import tortoise.models as models


class MiddlewareUtils:
    @staticmethod
    async def middleware(body: pydantic.BaseModel, **fields) -> pydantic.BaseModel:
        # user=None - del body.user || post=Post - Post.get(id=post)
        for name, model in fields.items():
            model: models.MODEL
            if model is None:
                delattr(body, name)
            else:
                setattr(body, name, await model.get(id=getattr(body, name)))
        return body


__all__ = [
    'MiddlewareUtils'
]
