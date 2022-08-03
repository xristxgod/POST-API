from fastapi import APIRouter


router = APIRouter(
    prefix="/user",
    tags=["USER"]
)


@router.post(
    "/registration"
)
async def registration():
    pass
