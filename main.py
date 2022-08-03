from fastapi import FastAPI

from src.models import database
from src.endpoints import router


app = FastAPI(
    description="",
    version="1.0.0"
)

app.include_router(router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8080)
