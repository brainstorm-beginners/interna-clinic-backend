from typing import Any, Sequence

from passlib.context import CryptContext

from app.api.v1.repositories.patient_repository import PatientRepository
from app.schemas.schemas import PatientRead, PatientUpdate, PatientCreateRawPassword, PatientCreateHashedPassword

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


class PatientService:
    def __init__(self, patient_repository: PatientRepository) -> None:
        self.patient_repository = patient_repository

    async def get_patients(self) -> Sequence[PatientRead]:
        """
        This method is used to retrieve all patients from the DB.

        Returns:
            patients (Sequence[Patient])
        """

        return await self.patient_repository.get_patients()

    async def get_patient_by_id(self, patient_id: int) -> PatientRead | None:
        """
        This method is used to retrieve a certain patient from the DB by his 'id' field.

        Returns:
            patients (Patient | None)
        """

        return await self.patient_repository.get_patient_by_id(patient_id)

    async def create_patient(self, raw_patient_data: PatientCreateRawPassword) -> dict[str, Any]:
        """
        This method is used to create a patient with the given data ('PatientCreate' model).
        Moreover, this method hashes the raw password.

        Returns:
            created patient (dict[str, Any])
        """

        hashed_password = hash_password(raw_patient_data.password)

        patient_data = raw_patient_data.model_dump()
        patient_data["hashed_password"] = hashed_password
        del patient_data["password"]

        patient_with_hashed_password = PatientCreateHashedPassword(**patient_data)

        return await self.patient_repository.create_patient(patient_with_hashed_password)

    async def update_patient(self, new_data_for_patient: PatientUpdate) -> PatientRead:
        """
        This method is used to update the existing patient data with the new one ('PatientUpdate' model).

        Returns:
            updated patient (dict[str, Any])
        """

        return await self.patient_repository.update_patient(new_data_for_patient)

    async def delete_patient(self, patient_id: int) -> int:
        """
        This method is used to delete the existing patient with given id.

        Returns:
            deleted patient ID (int)
        """

        return await self.patient_repository.delete_patient(patient_id)
