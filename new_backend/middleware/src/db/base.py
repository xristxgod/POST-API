from enum import Enum

from bson import ObjectId
from pydantic import BaseModel


class RatingEnum(Enum):
    SO_BAD = 0
    like = 1
    like = 2
    like = 3
    like = 4
    like = 5


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v == "":
            raise TypeError("ObjectId is empty")
        if not ObjectId.is_valid(v):
            raise TypeError("ObjectId invalid")
        return str(v)


class BaseDBModel(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        @classmethod
        def alias_generator(cls, string: str) -> str:
            """CamelCase generator"""
            temp = string.split("_")
            return temp[0] + "".join(ele.title() for ele in temp[1:])
