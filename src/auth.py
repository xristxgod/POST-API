from typing import Optional, Dict
from datetime import datetime, timedelta

import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .utils import utils
from .models import UserModel
from config import Config, logger


class AuthRepository:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AuthRepository, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.users: Dict = {}

    def add(self, user_id: int, token: str) -> Optional:
        if not self.users.get(user_id):
            self.users[user_id] = token
        else:
            if not AutoHandler.is_valid(self.users.get(user_id)):
                self.users[user_id] = AutoHandler.sign_jwt_token(user_id)

    def get(self, user_id: int) -> Optional[str]:
        return self.users.get(user_id)

    def delete(self, user_id: int) -> bool:
        if self.users.get(user_id):
            self.users.pop(user_id)
        return True


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
            flag = False
        try:
            UserModel.read(payload.get("userId"))
        except Exception:
            flag = False
        if not utils.is_time(payload.get("expireToken")):
            flag = False
        flag = True
        if not flag:
            auth_repository.delete(payload.get("userId"))
        return flag


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


auth_repository = AuthRepository()
