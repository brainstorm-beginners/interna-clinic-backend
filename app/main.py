import uvicorn
from fastapi import FastAPI
from app.api.v1.routers.patient_router import router as patient_router
from app.api.v1.routers.admin_router import router as admin_router
from app.api.v1.routers.doctor_router import router as doctor_router
from app.api.v1.auth.auth_router import router as auth_router

app = FastAPI()

app.include_router(patient_router)
app.include_router(admin_router)
app.include_router(doctor_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
