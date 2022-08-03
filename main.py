from fastapi import FastAPI

from src.endpoints import router


app = FastAPI(
    description="",
    version="1.0.0"
)

app.include_router(router)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
   pass


if __name__ == '__main__':
    import uvicorn
    # from src.models import create_db
    # print(create_db())
    uvicorn.run("main:app", port=8080)
