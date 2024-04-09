from typing import Any, Sequence

from fastapi import HTTPException
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

        patient = await self.patient_repository.get_patient_by_id(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail=f"Patient with id {patient_id} does not exist.")

        return patient

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

    async def update_patient(self, patient_id: int, new_data_for_patient: PatientUpdate) -> PatientRead:
        """
        This method is used to update the existing patient data with the new one ('PatientUpdate' model).

        Returns:
            updated patient (dict[str, Any])
        """

        patient_to_update = await self.patient_repository.get_patient_by_id(patient_id)
        if patient_to_update is None:
            raise HTTPException(status_code=404, detail=f"Patient with id {new_data_for_patient.id} does not exist.")

        return await self.patient_repository.update_patient(new_data_for_patient)

    async def delete_patient(self, patient_id: int) -> int:
        """
        This method is used to delete the existing patient with given id.

        Returns:
            deleted patient ID (int)
        """

        patient_to_delete = await self.patient_repository.get_patient_by_id(patient_id)
        if patient_to_delete is None:
            raise HTTPException(status_code=404, detail=f"Patient with id {patient_id} does not exist.")

        return await self.patient_repository.delete_patient(patient_id)
