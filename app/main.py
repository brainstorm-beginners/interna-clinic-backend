import uvicorn
from fastapi import FastAPI

from app.api.v1.routers.admin_router import router as admin_router

app = FastAPI()

app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
