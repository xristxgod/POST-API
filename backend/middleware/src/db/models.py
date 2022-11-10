from typing import Optional
from datetime import datetime

from pydantic import Field

from .base import BaseDBModel, OID, RatingEnum


class RatingPost(BaseDBModel):
    id: Optional[OID] = Field(description='Auth ID')
    status: RatingEnum = Field(description='Rating')
    created: datetime = Field(description='Created rating')
    updated: datetime = Field(description='Updated rating')

    PostId: int = Field(description='Post')
    userId: int = Field(description='User id')

    class Config:
        schema_extra = {
            "example": {
                'id': '6336dc765c423124e532c41d',
                'status': 4,
                'created': '2003-12-28T18:18:10-08:00',
                'updated': '2003-12-28T18:18:10-08:00',
                'postId': 45,
                'userId': 23,
            }
        }


class RatingComment(BaseDBModel):
    id: Optional[OID] = Field(description='Auth ID')
    status: RatingEnum = Field(description='Rating')
    created: datetime = Field(description='Created rating')
    updated: datetime = Field(description='Updated rating')

    CommentId: int = Field(description='Comment')
    userId: int = Field(description='User id')

    class Config:
        schema_extra = {
            "example": {
                'id': '63dc765c423123124e532c41d',
                'status': 5,
                'created': '2003-12-28T18:18:10-08:00',
                'updated': '2003-12-28T18:18:10-08:00',
                'commentId': 45,
                'userId': 23,
            }
        }


class RatingUser(BaseDBModel):
    id: Optional[OID] = Field(description='Auth ID')
    status: RatingEnum = Field(description='Rating')
    created: datetime = Field(description='Created rating')
    updated: datetime = Field(description='Updated rating')

    UserId: int = Field(description='Comment')
    userId: int = Field(description='User id')

    class Config:
        schema_extra = {
            "example": {
                'id': '63dc765c423123124e532c41d',
                'status': 5,
                'created': '2003-12-28T18:18:10-08:00',
                'updated': '2003-12-28T18:18:10-08:00',
                'commentId': 45,
                'userId': 23,
            }
        }
