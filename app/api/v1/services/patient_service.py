from typing import Any, Sequence

from fastapi import HTTPException
from passlib.context import CryptContext

from app.api.v1.repositories.patient_repository import PatientRepository
from app.api.v1.services.doctor_service import DoctorService
from app.schemas.schemas import PatientRead, PatientCreateRawPassword, PatientCreateHashedPassword, \
    PatientUpdateRawPassword, PatientUpdateHashedPassword

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


class PatientService:
    def __init__(self, patient_repository: PatientRepository, doctor_service: DoctorService) -> None:
        self.patient_repository = patient_repository
        self.doctor_service = doctor_service

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
            patient (PatientRead | None)
        """

        patient = await self.patient_repository.get_patient_by_id(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail=f"Patient with id {patient_id} does not exist.")

        return patient

    async def create_patient(self, raw_patient_data: PatientCreateRawPassword) -> dict[str, Any]:
        """
        This method is used to create a patient with the given data ('PatientCreateRawPassword' model).
        Moreover, this method:
        1). Hashes the raw password by creating new DICT with added 'hashed_password' field and
        deleted 'password' field. After this, it creates a new 'PatientCreateHashedPassword' object and sends it
        to the 'patient_repository'.
        2). Checking if patient with given IIN already exists in the DB.

        Returns:
            created patient data (dict[str, Any])

        Raises:
            HTTPException (409): if patient with given IIN already exists in the DB.
        """

        # Checking if patient with provided IIN already exists in the DB.
        already_existing_patient_with_provided_IIN = await self.patient_repository.get_patient_by_IIN(raw_patient_data.IIN)
        if already_existing_patient_with_provided_IIN:
            raise HTTPException(status_code=409, detail=f"Patient with IIN {raw_patient_data.IIN} already exists.")

        # Checking the presence of a patient's doctor in the DB
        await self.doctor_service.get_doctor_by_id(raw_patient_data.doctor_id)

        hashed_password = hash_password(raw_patient_data.password)

        patient_data = raw_patient_data.model_dump()
        patient_data["hashed_password"] = hashed_password
        del patient_data["password"]

        patient_with_hashed_password = PatientCreateHashedPassword(**patient_data)

        return await self.patient_repository.create_patient(patient_with_hashed_password)

    async def update_patient(self, patient_id: int, new_data_for_patient: PatientUpdateRawPassword) -> PatientRead:
        """
        This method is used to update the existing patient data with the new one ('PatientUpdate' model).

        Returns:
            updated patient (PatientRead)
        """

        patient_to_update = await self.patient_repository.get_patient_by_id(patient_id)
        if patient_to_update is None:
            raise HTTPException(status_code=404, detail=f"Patient with id {patient_id} does not exist.")

        hashed_password = hash_password(new_data_for_patient.password)

        patient_data = new_data_for_patient.model_dump()
        patient_data["hashed_password"] = hashed_password
        del patient_data["password"]

        patient_with_hashed_password = PatientUpdateHashedPassword(**patient_data)

        return await self.patient_repository.update_patient(patient_id, patient_with_hashed_password)

    async def delete_patient(self, patient_id: int) -> dict:
        """
        This method is used to delete the existing patient with given id.

        Returns:
            A dictionary containing the deleted patient ID and a message (dict).

        Raises:
            HTTPException (404): If the patient with given ID does not exist.
        """

        patient_to_delete = await self.patient_repository.get_patient_by_id(patient_id)
        if patient_to_delete is None:
            raise HTTPException(status_code=404, detail=f"Patient with id {patient_id} does not exist.")

        await self.patient_repository.delete_patient(patient_id)

        return {"patient_id": patient_id, "message": f"Patient with id {patient_id} has been deleted."}
