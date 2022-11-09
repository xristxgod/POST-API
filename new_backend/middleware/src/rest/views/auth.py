from fastapi import APIRouter


router = APIRouter()


@router.post(
    '/login'
)
async def login():
    pass


@router.post(
    '/registration'
)
async def registration():
    pass
