from typing import Any, Sequence

from fastapi import HTTPException
from passlib.context import CryptContext

from app.api.v1.repositories.doctor_repository import DoctorRepository
from app.schemas.schemas import DoctorRead, DoctorCreateRawPassword, DoctorCreateHashedPassword, \
    DoctorUpdateRawPassword, DoctorUpdateHashedPassword

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


class DoctorService:
    def __init__(self, doctor_repository: DoctorRepository) -> None:
        self.doctor_repository = doctor_repository

    async def get_doctors(self) -> Sequence[DoctorRead]:
        """
        This method is used to retrieve all doctors from the DB.

        Returns:
            doctors (Sequence[Patient])
        """

        return await self.doctor_repository.get_doctors()

    async def get_doctor_by_id(self, doctor_id: int) -> DoctorRead:
        """Retrieves a specific admin by ID."""
        doctor = await self.doctor_repository.get_doctor_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor

    async def create_doctor(self, raw_doctor_data: DoctorCreateRawPassword) -> dict[str, Any]:
        """
        This method is used to create a doctor with the given data ('DoctorCreateRawPassword' model).
        Moreover, this method hashes the raw password.

        Returns:
            created doctor (dict[str, Any])
        """

        hashed_password = hash_password(raw_doctor_data.password)

        doctor_data = raw_doctor_data.model_dump()
        doctor_data["hashed_password"] = hashed_password
        del doctor_data["password"]

        doctor_with_hashed_password = DoctorCreateHashedPassword(**doctor_data)

        return await self.doctor_repository.create_doctor(doctor_with_hashed_password)

    async def update_doctor(self, new_data_for_doctor: DoctorUpdateRawPassword, doctor_id: int) -> DoctorRead:
        """
        This method is used to update the existing doctor data with the new one ('DoctorUpdateRawPassword' model).

        Returns:
            updated doctor (dict[str, Any])
        """

        doctor_to_update = await self.doctor_repository.get_doctor_by_id(doctor_id)
        if doctor_to_update is None:
            raise HTTPException(status_code=404, detail=f"Patient with id {doctor_id} does not exist.")

        hashed_password = hash_password(new_data_for_doctor.password)

        doctor_data = new_data_for_doctor.model_dump()
        doctor_data["hashed_password"] = hashed_password
        del doctor_data["password"]

        doctor_with_hashed_password = DoctorUpdateHashedPassword(**doctor_data)

        return await self.doctor_repository.update_doctor(doctor_with_hashed_password, doctor_id)

    async def delete_doctor(self, doctor_id: int) -> int:
        """
        This method is used to delete the existing doctor with given id.

        Returns:
            deleted doctor ID (int)
        """

        return await self.doctor_repository.delete_doctor(doctor_id)
