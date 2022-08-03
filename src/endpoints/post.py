from fastapi import APIRouter, Depends, Request

from ..auth import JWTBearer, AutoHandler
from ..models import PostModel
from ..base.schemas import BodyModPost, DataCreatePost, QueryPost, ResponsePost, ResponseStatus


router = APIRouter(
    prefix="/post",
    tags=["Post"]
)


@router.post(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseStatus
)
async def create_post(request: Request, body: BodyModPost):
    """
    Create new post

    - **title**: post title (optional)
    - **text**: post text (optional)
    """
    return ResponseStatus(status=PostModel.create(data=DataCreatePost(
        title=body.title,
        text=body.text,
        authorId=AutoHandler.decode_jwt_token(request.headers.get("Authorization").split(" ")[1]).get("userId")
    )))


@router.get(
    "/",
    response_model=ResponsePost
)
async def get_post(query: QueryPost = Depends()):
    """
    Get post by id

    - **postId**: post id
    """
    return PostModel.read(query.postId)


@router.put(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseStatus
)
async def update_post(request: Request, body: BodyModPost, query: QueryPost = Depends()):
    """
    Update post

    - **title**: post title (optional)
    - **text**: post text (optional)
    """


@router.delete(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponsePost
)
async def get_post(query: QueryPost = Depends()):
    """
    Delete post by id

    - **postId**: post id
    """
    # return PostModel.read(query.postId)