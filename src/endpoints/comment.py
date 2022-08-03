from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException

from ..auth import JWTBearer, AutoHandler
from ..models import CommentModel, session
from ..base.schemas import QueryPost, QueryComment, BodyModComment, ResponseComment, ResponseStatus, DataComment


router = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)


@router.get(
    "/all/",
    response_model=List[ResponseComment]
)
async def get_all_comments_by_post(query: QueryPost = Depends()):
    """
    Get all comments by post

    - **postId**: post id
    """
    return [
        ResponseComment(
            id=comment.id,
            text=comment.text,
            parentId=comment.parent_id,
            parentCommentId=comment.parent_comment_id,
            postId=comment.post_id,
            createAt=comment.create_at,
            updateAt=comment.update_at,
            authorId=comment.author_id
        )
        for comment in session.query(CommentModel).filter_by(post_id=query.postId).all()
    ]


@router.get(
    "/user/all",
    dependencies=[Depends(JWTBearer())],
    response_model=List[ResponseComment]
)
async def get_all_comments_by_user_id(request: Request):
    """
    Get all comments by user id
    """
    user_id = AutoHandler.decode_jwt_token(request.headers.get("Authorization").split(" ")[1])["userId"]
    return [
        ResponseComment(
            id=comment.id,
            text=comment.text,
            parentId=comment.parent_id,
            parentCommentId=comment.parent_comment_id,
            postId=comment.post_id,
            createAt=comment.create_at,
            updateAt=comment.update_at,
            authorId=comment.author_id
        )
        for comment in session.query(CommentModel).filter_by(author_id=user_id).all()
    ]


@router.post(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseStatus
)
async def create_comment(request: Request, body: BodyModComment, query: QueryPost = Depends()):
    """
    Create new comment by post id

    - **text**: post text
    - **postId**: post id
    - **parentId**: ID of the person whose comment was answered! (optional)
    """
    return ResponseStatus(status=CommentModel.create(data=DataComment(
        text=body.text,
        parentId=body.parentId,
        parentCommentId=body.parentCommentId,
        postId=query.postId,
        authorId=AutoHandler.decode_jwt_token(request.headers.get("Authorization").split(" ")[1])["userId"]
    )))


@router.get(
    "/",
    response_model=ResponseComment
)
async def get_comment(query: QueryComment = Depends()):
    """
    Get comment by id

    - **commentId**: comment id
    """
    return CommentModel.read(comment_id=query.commentId)


@router.put(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseStatus
)
async def update_comment(request: Request, body: BodyModComment, query: QueryComment = Depends()):
    """
    Update comment

    - **commentId**: comment id
    - **text**: comment text
    """
    user_id = AutoHandler.decode_jwt_token(request.headers.get("Authorization").split(" ")[1])["userId"]
    if CommentModel.read(query.commentId).authorId != user_id:
        raise HTTPException(detail="You are not the owner of the comment!", status_code=401)
    return ResponseStatus(status=CommentModel.update(data=DataComment(text=body.text)))


@router.delete(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseStatus
)
async def delete_comment(request: Request, query: QueryComment = Depends()):
    """
    Delete comment by id

    - **commentId**: post id
    """
    user_id = AutoHandler.decode_jwt_token(request.headers.get("Authorization").split(" ")[1])["userId"]
    if CommentModel.read(query.commentId).authorId != user_id:
        raise HTTPException(detail="You are not the owner of the comment!", status_code=401)
    return CommentModel.delete(query.commentId)
