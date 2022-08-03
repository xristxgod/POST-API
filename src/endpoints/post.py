from fastapi import APIRouter


router = APIRouter(
    prefix="/post",
    tags=["POST"]
)


@router.post(
    "/"
)
async def create_post():
    pass
