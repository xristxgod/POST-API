import tortoise
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from src.rest.views import api


app = fastapi.FastAPI()

app.include_router(api, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[''],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    register_tortoise(
        app=app,
        db_url='sqlite://db.sqlite3',
        modules={'models': ['src.db.models']},
        generate_schemas=True,
        add_exception_handlers=True,
    )


@app.on_event("shutdown")
async def shutdown():
    await tortoise.Tortoise.close_connections()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app')
