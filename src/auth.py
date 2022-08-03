from typing import Dict
from datetime import datetime, timedelta

import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .models import UserModel
from config import Config, logger


class AutoHandler:
    @staticmethod
    def sign_jwt_token(user_id: int) -> Dict[str, str]:
        return jwt.encode({
            "userId": user_id,
            "createToken": str(datetime.now()),
            "expireToken": str(datetime.now() + timedelta(days=2))
        }, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

    @staticmethod
    def decode_jwt_token(token: str) -> Dict:
        try:
            return jwt.decode(token, Config.JWT_SECRET, algorithms=Config.JWT_ALGORITHM)
        except Exception as error:
            logger.error(f"{error}")
            return {}

    @staticmethod
    def is_valid(token: str) -> bool:
        payload = AutoHandler.decode_jwt_token(token)
        if not payload:
            return False
        # {'userId': 12, 'createToken': '2022-08-03 10:06:57.502828', 'expireToken': '2022-08-05 10:06:57.502828'}
        try:
            UserModel.read(payload.get("userId"))
        except Exception:
            return False
        return True


class JWTBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid token!")
            if not AutoHandler.is_valid(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token!")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid token!")
