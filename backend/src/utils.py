import os
import io
from typing import Union, List

import bcrypt
import aiofiles

import src.settings as settings


class Password:

    @staticmethod
    def hash(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def valid(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())


class Default:

    @staticmethod
    def default_image() -> io.BytesIO:
        async with aiofiles.open(os.path.join(settings.DEFAULT_DIR, 'no-photos.png'), 'rb') as raw_avatar:
            return io.BytesIO(await raw_avatar.read())
