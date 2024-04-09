import uvicorn
from fastapi import FastAPI
from app.api.v1.routers.patient_router import router as patient_router

from app.api.v1.routers.admin_router import router as admin_router

app = FastAPI()

app.include_router(patient_router)


# TODO: Delete or change this endpoint (it's for testing only)
@app.get("/")
async def home():
    return {"data": "Hello World"}

app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
