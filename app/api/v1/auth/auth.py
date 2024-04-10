from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.models.models import Patient, Doctor, Admin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_patient(patient_IIN: str, patient_raw_password: str, session: AsyncSession):
    data = await session.execute(select(Patient).where(Patient.IIN == patient_IIN))
    patient = data.scalars().first()

    if not patient:
        return False
    if not verify_password(patient_raw_password, patient.hashed_password):
        return False

    return patient


async def authenticate_doctor(doctor_IIN: str, doctor_raw_password: str, session: AsyncSession):
    data = await session.execute(select(Doctor).where(Doctor.IIN == doctor_IIN))
    doctor = data.scalars().first()

    if not doctor:
        return False
    if not verify_password(doctor_raw_password, doctor.hashed_password):
        return False

    return doctor


async def authenticate_admin(admin_username: str, admin_raw_password: str, session: AsyncSession):
    data = await session.execute(select(Admin).where(Admin.username == admin_username))
    admin = data.scalars().first()

    if not admin:
        return False
    if not verify_password(admin_raw_password, admin.hashed_password):
        return False

    return admin
