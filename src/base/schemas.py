from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator


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


class BodyCreatePost(BaseModel):
    title: Optional[str] = Field(description="Post title", max_length=50, default=None)
    text: Optional[str] = Field(description="Post text", default=None)
    authorId: int = Field(description="Post author")

    @validator("authorId")
    def valid_author_id(cls, author_id: int):
        pass

    @validator("title")
    def valid_title_id(cls, title: str):
        pass

    @validator("text")
    def valid_text_id(cls, text: str):
        pass


class BodyCreateComment(BaseModel):
    text: str
    parentId: int
    postId: int
    authorId: int


# <<<=======================================>>> Response <<<=========================================================>>>


class ResponseCreateUser(BaseModel):
    status: bool = Field(description="Status registration")

    class Config:
        schema_extra = {
            "example": {
                "status": True
            }
        }


class ResponseLoginUser(BaseModel):
    successLogin: bool = Field()
    username: str = Field()
    token: str = Field()
    expireToken: datetime = Field()

    class Config:
        schema_extra = {
            "example": {
                "successLogin": True,
                "username": "root",
                "token": "EYwuqFJmFuuqZq6zpcb7PMah2SbKTMkY",
                "expireToken": datetime.now()
            }
        }
