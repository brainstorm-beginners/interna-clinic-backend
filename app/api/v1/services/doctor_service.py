from typing import Any, Sequence

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from app.api.v1.repositories.doctor_repository import DoctorRepository
from app.schemas.schemas import DoctorRead, DoctorCreateRawPassword, DoctorCreateHashedPassword, \
    DoctorUpdateRawPassword, DoctorUpdateHashedPassword, PatientRead

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
            doctors (Sequence[DoctorRead])
        """

        return await self.doctor_repository.get_doctors()

    async def get_doctor_by_id(self, doctor_id: int) -> DoctorRead:
        """
        This method is used to retrieve a certain doctor from the DB by his 'id' field.

        Returns:
            doctor (DoctorRead | None)

        Raises:
            HTTPException (404): if the doctor with given ID does not exist.
        """

        doctor = await self.doctor_repository.get_doctor_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail=f"Doctor with id {doctor_id} doest not exist.")

        return doctor

    async def get_doctor_patients(self, doctor_id: int) -> Sequence[PatientRead]:
        """
        Retrieve list of doctor's patients, assigned to the doctor with this ID.

        Argument:
            doctor_id (int): Doctor ID

        Returns:
            Sequence[PatientRead]: List of patients, assigned to the doctor
        """
        existing_doctor = await self.get_doctor_by_id(doctor_id)
        if not existing_doctor:
            raise HTTPException(status_code=404, detail=f"Doctor with id {doctor_id} does not exist.")

        doctor_patients = await self.doctor_repository.get_doctor_patients(doctor_id)
        return doctor_patients

    async def create_doctor(self, raw_doctor_data: DoctorCreateRawPassword) -> dict[str, Any]:
        """
        This method is used to create a doctor with the given data ('DoctorCreateRawPassword' model).
        Moreover, this method:
        1). Hashes the raw password by creating new DICT with added 'hashed_password' field and
        deleted 'password' field. After this, it creates a new 'DoctorCreateHashedPassword' object and sends it
        to the 'doctor_repository'.
        2). Checking if doctor with given IIN already exists in the DB.

        Returns:
            created doctor data (dict[str, Any])

        Raises:
            HTTPException (409): if doctor with given IIN already exists in the DB.
        """

        # Checking if doctor with provided IIN already exists in the DB.
        already_existing_doctor_with_provided_IIN = await self.doctor_repository.get_doctor_by_IIN(raw_doctor_data.IIN)
        if already_existing_doctor_with_provided_IIN:
            raise HTTPException(status_code=409, detail=f"Doctor with IIN {raw_doctor_data.IIN} already exists.")

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
            updated doctor (DoctorRead)
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

    async def delete_doctor(self, doctor_id: int) -> dict:
        """
        This method is used to delete the existing doctor with given id.

        Returns:
            A dictionary containing the deleted doctor ID and a message (dict)

        Raises:
            HTTPException (404): if doctor with given ID does not exist.
            HTTPException (409): if doctor with given ID cannot be deleted because of relationship with
            existing patients.
        """

        doctor_to_delete = await self.doctor_repository.get_doctor_by_id(doctor_id)
        if doctor_to_delete is None:
            raise HTTPException(status_code=404, detail=f"Doctor with id {doctor_id} does not exist.")

        try:
            await self.doctor_repository.delete_doctor(doctor_id)
            return {"doctor_id": doctor_id, "message": f"Doctor with id {doctor_id} has been deleted."}
        except IntegrityError:
            raise HTTPException(status_code=409,
                                detail=f"Doctor with id {doctor_id} cannot be deleted because they have associated "
                                       f"patients.")
