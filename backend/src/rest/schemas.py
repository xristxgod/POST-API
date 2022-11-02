from typing import Optional

from pydantic import BaseModel, Field, validator, constr


class ModUser(BaseModel):
    username: Optional[constr(max_length=255, min_length=5)]
    password_hash: Optional[constr(max_length=255, min_length=5)] = Field(alias='password')
    active: Optional[bool] = Field(default=True)

    @validator('username')
    def valid_username(cls, username: str):
        if not username.startswith('@'):
            username = '@' + username
        return username

    class Config:
        schema_extra = {
            "example": {
                "username": "@muro.bodriy",
                "password": "12341fvasd231",
                "active": True,
            }
        }


class ModPost(BaseModel):
    title: Optional[constr(max_length=255, min_length=5)]
    text: Optional[constr(min_length=50)]
    video_link: Optional[str] = Field(alias='videoLink')
    active: Optional[bool] = Field(default=True)
    user: Optional[int] = Field(alias='userId')

    @validator('videoLink', check_fields=False)
    def valid_video_link(cls, video_link: str):
        return video_link

    class Config:
        schema_extra = {
            "example": {
                "title": "My new post",
                "text": "This is the primary way of converting a model to a dictionary. Sub-models will be recursively",
                "videoLink": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "active": True,
                "userId": 12
            }
        }


class ModComment(BaseModel):
    text: Optional[constr(max_length=255, min_length=5)]
    post: Optional[int] = Field(alias='postId')
    user: Optional[int] = Field(alias='userId')
    sub_comment: Optional[int] = Field(alias='subComment')

    @validator('text')
    def valid_text(cls, text: str):
        ...
        return text

    @validator('subComment')
    def valid_sub_comment(self, sub_comment: int):
        # user != sub_comment
        ...
        return sub_comment

    class Config:
        schema_extra = {
            "example": {
                "text": "This is the primary way of converting a model to a dictionary. Sub-models will be recursively",
                "postId": 12,
                "userId": 12
            }
        }


class ResponseSuccessfully(BaseModel):
    successfully: bool = Field(default=True)

    class Config:
        schema_extra = {
            "example": {
                "successfully": True
            }
        }


class ResponseMessage(BaseModel):
    message: str = Field(default='Not found')

    class Config:
        schema_extra = {
            "example": {
                "message": "Not found"
            }
        }