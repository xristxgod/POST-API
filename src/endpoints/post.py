from fastapi import APIRouter, Depends, Request

from ..auth import JWTBearer, AutoHandler
from ..models import PostModel
from ..base.schemas import BodyCreatePost, ResponseStatus


router = APIRouter(
    prefix="/post",
    tags=["POST"]
)


@router.post(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseStatus
)
async def create_post(request: Request, body: BodyCreatePost):
    """
    Create new post

    - **title**: post title (optional)
    - **text**: post text (optional)
    """
    body.authorId = AutoHandler.decode_jwt_token(request.headers.get("Authorization").split(" ")[1]).get("userId")
    print(body)
    # return ResponseStatus(status=PostModel.create(data=body))
