import io
from typing import Union, List

import bcrypt
from fastapi.responses import StreamingResponse


class Password:

    @staticmethod
    def hash(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def valid(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())


class CustomResponses:

    @staticmethod
    def image_response(img: Union[List[bytes], bytes]) -> Union[List[StreamingResponse], StreamingResponse]:
        if isinstance(img, bytes):
            return StreamingResponse(io.BytesIO(img), media_type="image/png")

        for image in img:
            yield StreamingResponse(io.BytesIO(image), media_type="image/png")
