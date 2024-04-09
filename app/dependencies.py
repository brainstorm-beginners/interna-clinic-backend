from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.repositories.admin_repository import AdminRepository
from app.api.v1.repositories.patient_repository import PatientRepository
from app.api.v1.services.admin_service import AdminService
from app.api.v1.services.patient_service import PatientService
from app.config.database import async_session_maker


async def get_async_session():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


def get_patient_service(session: AsyncSession = Depends(get_async_session)) -> PatientService:
    patient_repository = PatientRepository(session)
    return PatientService(patient_repository)


def get_admin_service(session: AsyncSession = Depends(get_async_session)) -> AdminService:
    admin_repository = AdminRepository(session)
    return AdminService(admin_repository)
