import uvicorn
from fastapi import FastAPI

from api.router import api_router as todo_router

app = FastAPI(
    title="ToDo API",
    openapi_url="/todo/openapi.json",
    docs_url="/todo/docs",
)


app.include_router(todo_router, prefix="/todo")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
    )
