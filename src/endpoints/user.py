from fastapi import APIRouter, Depends, Request, HTTPException

from ..auth import JWTBearer, AutoHandler, auth_repository
from ..base.schemas import DataUser, BodyModUser, ResponseStatus, BodyLoginUser, ResponseLoginUser, ResponseUser
from ..models import UserModel, session


router = APIRouter()


@router.post(
    "/registration",
    response_model=ResponseStatus,
    tags=["Authorization"]
)
async def registration(body: BodyModUser):
    """
    Registration new user

    - **username**: user username
    - **password**: user password
    - **firstName**: first name (optional)
    - **lastName**: last name (optional)
    """
    return ResponseStatus(status=UserModel.create(data=body))


@router.post(
    "/login",
    response_model=ResponseLoginUser,
    tags=["Authorization"]
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
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseUser,
    tags=["User"]
)
async def get_current_user(request: Request):
    """
    Get information about an authorized user
    """
    return UserModel.read(
        AutoHandler.decode_jwt_token(request.headers.get("Authorization").split(" ")[1]).get("userId")
    )


@router.put(
    "/user",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseStatus,
    tags=["User"]
)
async def update_user(request: Request, body=BodyModUser):
    """
    Update user info

    - **username**: user username
    - **password**: user password
    - **firstName**: first name
    - **lastName**: last name
    """
    return ResponseStatus(status=UserModel.update(data=DataUser(
        userId=AutoHandler.decode_jwt_token(request.headers.get("Authorization").split(" ")[1])["userId"],
        username=body.username,
        password=body.password,
        firstName=body.firstName,
        lastName=body.lastName
    )))


@router.delete(
    "/user",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseStatus,
    tags=["User"]
)
async def delete_user(request: Request):
    """
    Delete user by id
    :param request:
    :return:
    """
    user_id = AutoHandler.decode_jwt_token(request.headers.get("Authorization").split(" ")[1])["userId"]
    status = ResponseStatus(status=UserModel.delete(user_id=user_id,))
    auth_repository.delete(user_id)
    return status
