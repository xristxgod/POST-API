from pydantic import BaseModel


class BodyUser(BaseModel):
    username: str
    password: str
    lastName: str
    firstName: str


class BodyPost(BaseModel):
    title: str
    text: str
    authorId: int


class BodyComment(BaseModel):
    text: str
    parentId: int
    postId: int
    authorId: int
