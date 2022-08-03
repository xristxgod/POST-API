from typing import Optional
from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel, Field, validator


# <<<=======================================>>> Dataclasses <<<======================================================>>>


@dataclass()
class DataCreatePost:
    title: str
    text: str
    authorId: str


# <<<=======================================>>> Query <<<============================================================>>>


class QueryPost(BaseModel):
    postId: int = Field(description="Post id")


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


class BodyCreateComment(BaseModel):
    text: str
    parentId: int
    postId: int
    authorId: int


# <<<=======================================>>> Response <<<=========================================================>>>


class ResponseStatus(BaseModel):
    status: bool = Field(description="Status")

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
    username: str = Field(description="Username", max_length=50, min_length=4)
    password: str = Field(description="Password", max_length=50, min_length=8)
    firstName: Optional[str] = Field(description="First name", max_length=50, default=None)
    lastName: Optional[str] = Field(description="Last name", max_length=50, default=None)

    class Config:
        schema_extra = {
            "example": {
                "username": "root",
                "password": "0000",
                "firstName": "Murad",
                "lastName": "Mamedov",
            }
        }


class ResponsePost(BaseModel):
    title: str = Field(description="Post title", max_length=50)
    text: str = Field(description="Post text")
    createAt: datetime = Field(description="Create time")
    updateAt: datetime = Field(description="Update time")
    authorId: Optional[int] = Field(description="Author id", default=None)

    class Config:
        schema_extra = {
            "example": {
                "title": "New PC",
                "text": "This is my new pc and i love play video game! ...",
                "createAt": "2022-08-03 14:34:07.613685",
                "updateAt": "2022-08-03 14:34:07.613685",
                "authorId": 666
            }
        }
