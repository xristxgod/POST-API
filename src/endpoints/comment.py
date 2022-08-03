from fastapi import APIRouter


router = APIRouter(
    prefix="/comment",
    tags=["COMMENT"]
)


@router.post(
    "/"
)
async def create_comment():
    pass
