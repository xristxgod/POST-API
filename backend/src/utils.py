import io
from typing import Union, List

import bcrypt
from fastapi.responses import StreamingResponse
from fastapi import HTTPException, status


class Password:

    @staticmethod
    def hash(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def valid(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())


class CustomResponses:

    @staticmethod
    def images_response(img: bytes) -> StreamingResponse:
        try:
            return StreamingResponse(io.BytesIO(img), media_type='image/png')
        except TypeError:
            raise HTTPException(detail='Not found', status_code=status.HTTP_404_NOT_FOUND)
