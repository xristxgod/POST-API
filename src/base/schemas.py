from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass, field

from pydantic import BaseModel, Field, validator


# <<<=======================================>>> Dataclasses <<<======================================================>>>


@dataclass()
class DataPost:
    postId: Optional[int] = field(default=None)
    title: Optional[str] = field(default=None)
    text: Optional[str] = field(default=None)
    authorId: Optional[int] = field(default=None)


@dataclass()
class DataComment:
    commentId: Optional[int] = field(default=None)
    text: Optional[str] = field(default=None)
    parentId: Optional[int] = field(default=None)
    postId: Optional[int] = field(default=None)
    authorId: Optional[int] = field(default=None)


# <<<=======================================>>> Query <<<============================================================>>>


class QueryPost(BaseModel):
    postId: int = Field(description="Post id")


class QueryComment(BaseModel):
    commentId: int = Field(description="Post id")


# <<<=======================================>>> Body <<<=============================================================>>>


class BodyCreateUser(BaseModel):
    username: str = Field(description="Username", max_length=50, min_length=4)
    password: str = Field(description="Password", max_length=50, min_length=8)
    firstName: Optional[str] = Field(description="First name", max_length=50, default=None)
    lastName: Optional[str] = Field(description="Last name", max_length=50, default=None)

    @validator("firstName")
    def valid_first_name(cls, first_name: str):
        if isinstance(first_name, str):
            return first_name.title()
        raise ValueError("First name must be a string!")

    @validator("lastName")
    def valid_last_name(cls, last_name: str):
        if isinstance(last_name, str):
            return last_name.title()
        raise ValueError("Last name must be a string!")

    class Config:
        schema_extra = {
            "example": {
                "username": "root",
                "password": "0000",
                "firstName": "Murad",
                "lastName": "Mamedov",
            }
        }


class BodyLoginUser(BaseModel):
    username: str = Field(description="Username", max_length=50, min_length=4)
    password: str = Field(description="Password", max_length=50, min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "username": "root",
                "password": "0000"
            }
        }


class BodyModPost(BaseModel):
    title: Optional[str] = Field(description="Post title", max_length=50, default=None)
    text: Optional[str] = Field(description="Post text", default=None)

    @validator("title")
    def valid_title_id(cls, title: str):
        if isinstance(title, str):
            return title.title()
        raise ValueError("Title must be a string!")

    class Config:
        schema_extra = {
            "example": {
                "title": "New PC",
                "text": "This is my new pc and i love play video game! ...",
            }
        }


class BodyModComment(BaseModel):
    text: Optional[str] = Field(description="Comment text", default=None)
    parentId: Optional[int] = Field(description="ID of the person whose comment was answered!", default=None)

    class Config:
        schema_extra = {
            "example": {
                "text": "This is a good post!",
                "parentId": 1,
            }
        }


# <<<=======================================>>> Response <<<=========================================================>>>


class ResponseStatus(BaseModel):
    status: bool = Field(description="Status", default=True)

    class Config:
        schema_extra = {
            "example": {
                "status": True
            }
        }


class ResponseLoginUser(BaseModel):
    token: str = Field(description="Authorization token")

    class Config:
        schema_extra = {
            "example": {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
            }
        }


class ResponseUser(BaseModel):
    id: int = Field(description="User ID")
    username: str = Field(description="Username", max_length=50, min_length=4)
    password: str = Field(description="Password", max_length=50, min_length=8)
    firstName: Optional[str] = Field(description="First name", max_length=50, default=None)
    lastName: Optional[str] = Field(description="Last name", max_length=50, default=None)

    class Config:
        schema_extra = {
            "example": {
                "id": 666,
                "username": "root",
                "password": "0000",
                "firstName": "Murad",
                "lastName": "Mamedov",
            }
        }


class ResponseComment(BaseModel):
    id: int = Field(description="Comment ID")
    text: str = Field(description="Comment text")
    parentId: Optional[int] = Field(description="ID of the person whose comment was answered!", default=None)
    postId: int = Field(description="Post id")
    createAt: datetime = Field(description="Create comment time")
    updateAt: datetime = Field(description="Update comment time")
    authorId: Optional[int] = Field(description="The author of the comment", default=None)

    class Config:
        schema_extra = {
            "example": {
                "id": 14,
                "text": "This is a good post",
                "parentId": 55,
                "postId": 1,
                "createAt": "2022-08-03 14:34:07.613685",
                "updateAt": "2022-08-03 14:34:07.613685",
                "authorId": 666
            }
        }


class ResponsePost(BaseModel):
    id: int = Field(description="Post ID")
    title: str = Field(description="Post title", max_length=50)
    text: str = Field(description="Post text")
    createAt: datetime = Field(description="Create time")
    updateAt: datetime = Field(description="Update time")
    authorId: Optional[int] = Field(description="Author id", default=None)
    comments: Optional[List[ResponseComment]] = Field(description="Comments", default=[])

    class Config:
        schema_extra = {
            "example": {
                "id": 15,
                "title": "New PC",
                "text": "This is my new pc and i love play video game! ...",
                "createAt": "2022-08-03 14:34:07.613685",
                "updateAt": "2022-08-03 14:34:07.613685",
                "authorId": 666,
                "comments": [
                    {
                        "id": 14,
                        "text": "This is a good post",
                        "parentId": 55,
                        "postId": 1,
                        "createAt": "2022-08-03 14:34:07.613685",
                        "updateAt": "2022-08-03 14:34:07.613685",
                        "authorId": 666
                    }
                ]
            }
        }
