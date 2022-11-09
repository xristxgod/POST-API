from fastapi import APIRouter


router = APIRouter()


@router.post(
    '/'
)
async def set_rating():
    pass


@router.get(
    '/'
)
async def get_ratings():
    pass


@router.put(
    '/'
)
async def update_rating():
    pass


@router.delete(
    '/'
)
async def delete_rating():
    pass
