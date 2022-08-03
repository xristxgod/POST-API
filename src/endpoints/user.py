from fastapi import APIRouter

from ..base.schemas import BodyUser, ResponseCreateUser
from ..models import UserModel


router = APIRouter()


@router.post(
    "/registration",
    tags=["Authorization"],
    response_model=ResponseCreateUser
)
async def registration(body: BodyUser):
    """
    Registration new user

    - **username**: user username
    - **password**: user password
    - **firstName**: first name
    - **lastName**: last name
    """
    return ResponseCreateUser(status=UserModel.create(data=body))
