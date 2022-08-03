from typing import List

from fastapi import APIRouter, Depends, Request

from ..auth import JWTBearer, AutoHandler
from ..models import CommentModel, session
from ..base.schemas import QueryPost, BodyCreateComment, ResponseComment, ResponseStatus, DataComment


router = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)


@router.get(
    "/all/",
    response_model=List[ResponseComment]
)
async def get_all_comments_by_post(query: QueryPost = Depends()):
    pass


@router.get(
    "/user/all",
    dependencies=[Depends(JWTBearer())],
    response_model=List[ResponseComment]
)
async def get_all_comments_by_id():
    pass


@router.post(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseStatus
)
async def create_comment(request: Request, body: BodyCreateComment, query: QueryPost = Depends()):
    """
    Create new comment by post id

    - **text**: post text
    - **postId**: post id
    - **parentId**: ID of the person whose comment was answered! (optional)
    """
    return ResponseStatus(status=CommentModel.create(data=DataComment(
        text=body.text,
        parentId=body.parentId,
        postId=query.postId,
        authorId=AutoHandler.decode_jwt_token(request.headers.get("Authorization").split(" ")[1])["userId"]
    )))


@router.get(
    "/",
    response_model=ResponseComment
)
async def get_comment():
    pass


@router.put(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseStatus
)
async def update_comment():
    pass


@router.delete(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseStatus
)
async def delete_comment():
    pass
