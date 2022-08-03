from fastapi import APIRouter, Depends, Request

from ..auth import JWTBearer, AutoHandler
from ..models import CommentModel, session
from ..base.schemas import QueryPost, BodyCreateComment, ResponseComment, ResponseStatus, DataComment


router = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)


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
