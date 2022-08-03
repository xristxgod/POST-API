from fastapi import APIRouter, HTTPException

from ..auth import AutoHandler, auth_repository
from ..base.schemas import BodyCreateUser, ResponseCreateUser, BodyLoginUser, ResponseLoginUser, ResponseUser
from ..models import UserModel, session


router = APIRouter(
    tags=["Authorization"]
)


@router.post(
    "/registration",
    response_model=ResponseCreateUser
)
async def registration(body: BodyCreateUser):
    """
    Registration new user

    - **username**: user username
    - **password**: user password
    - **firstName**: first name (optional)
    - **lastName**: last name (optional)
    """
    return ResponseCreateUser(status=UserModel.create(data=body))


@router.post(
    "/login",
    response_model=ResponseLoginUser
)
async def login(body: BodyLoginUser):
    """
    Login user

    - **username**: user username
    - **password**: user password
    """
    user = session.query(UserModel).filter_by(username=body.username).first()
    if not user:
        raise HTTPException(detail="User not found in the system!", status_code=401)
    if user.password != body.password:
        raise HTTPException(detail="Invalid password!", status_code=401)
    auth_repository.add(
        user_id=user.id,
        token=AutoHandler.sign_jwt_token(user.id)
    )
    return ResponseLoginUser(
        token=auth_repository.get(user_id=user.id)
    )


@router.get(
    "/user/me",
    response_model=ResponseUser
)
async def get_current_user():
    pass
