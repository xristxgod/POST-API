from fastapi import APIRouter

from ..base.schemas import BodyCreateUser, ResponseCreateUser, BodyLoginUser, ResponseLoginUser
from ..models import UserModel


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



