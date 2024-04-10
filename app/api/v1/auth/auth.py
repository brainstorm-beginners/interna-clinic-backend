from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.models.models import Patient, Doctor, Admin
from app.schemas.schemas import PatientRead, DoctorRead, AdminRead

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    This method is used to verify the identity of the raw and encrypted password in the DB.

    Returns:
        True or False (bool)
    """

    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_patient(patient_IIN: str, patient_raw_password: str, session: AsyncSession) -> PatientRead | bool:
    """
    This method is used to authenticate a patient by checking theirs presence in the DB and verifying raw password
    with hashed password in the DB.

    Returns:
        patient or False (PatientRead | bool)
    """

    data = await session.execute(select(Patient).where(Patient.IIN == patient_IIN))
    patient = data.scalars().first()

    if not patient:
        return False
    if not verify_password(patient_raw_password, patient.hashed_password):
        return False

    return patient


async def authenticate_doctor(doctor_IIN: str, doctor_raw_password: str, session: AsyncSession) -> DoctorRead | bool:
    """
    This method is used to authenticate a doctor by checking theirs presence in the DB and verifying raw password
    with hashed password in the DB.

    Returns:
        doctor or False (DoctorRead | bool)
    """

    data = await session.execute(select(Doctor).where(Doctor.IIN == doctor_IIN))
    doctor = data.scalars().first()

    if not doctor:
        return False
    if not verify_password(doctor_raw_password, doctor.hashed_password):
        return False

    return doctor


async def authenticate_admin(admin_username: str, admin_raw_password: str, session: AsyncSession) -> AdminRead | bool:
    """
    This method is used to authenticate an admin by checking theirs presence in the DB and verifying raw password
    with hashed password in the DB.

    Returns:
        admin or False (AdminRead | bool)
    """

    data = await session.execute(select(Admin).where(Admin.username == admin_username))
    admin = data.scalars().first()

    if not admin:
        return False
    if not verify_password(admin_raw_password, admin.hashed_password):
        return False

    return admin
