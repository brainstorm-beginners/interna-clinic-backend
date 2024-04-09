from typing import Sequence, Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Patient
from app.schemas.schemas import PatientUpdate, PatientRead, PatientCreateHashedPassword


class PatientRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_patients(self) -> Sequence[PatientRead]:
        """
        This method is used to retrieve all patients from the DB.

        Returns:
            patients (Sequence[PatientRead])
        """

        data = await self.session.execute(select(Patient))
        patients = data.scalars().all()

        return patients

    async def get_patient_by_id(self, patient_id: int) -> PatientRead | None:
        """
        This method is used to retrieve a certain patient from the DB by his 'id' field.

        Returns:
            patients (Patient | None)
        """

        data = await self.session.execute(select(Patient).where(Patient.id == patient_id))
        patient = data.scalars().first()

        return patient

    async def create_patient(self, new_patient_data: PatientCreateHashedPassword) -> dict[str, Any]:
        """
        This method is used to create a patient with the given data ('PatientCreate' model).

        Returns:
            created patient (dict[str, Any])
        """

        new_patient = Patient(**new_patient_data.model_dump())
        self.session.add(new_patient)
        await self.session.flush()
        await self.session.commit()

        return new_patient

    async def update_patient(self, new_data_for_patient: PatientUpdate) -> PatientRead:
        """
        This method is used to update the existing patient data with the new one ('PatientUpdate' model).

        Returns:
            updated patient (dict[str, Any])

        Raises:
            HTTPException: If the patient with the given ID is not found.
        """

        patient_to_update = await self.get_patient_by_id(new_data_for_patient.id)
        if patient_to_update is None:
            raise HTTPException(status_code=404, detail=f"Patient with id {new_data_for_patient.id} does not exist.")

        patient_to_update.update_field(new_data_for_patient.model_dump())

        await self.session.flush()
        await self.session.commit()

        return patient_to_update

    async def delete_patient(self, patient_id: int) -> int:
        """
        This method is used to delete the existing patient with given ID.

        Returns:
            deleted patient ID (int)

        Raises:
            HTTPException: If the patient with the given ID is not found.
        """

        patient_to_delete = await self.get_patient_by_id(patient_id)
        if patient_to_delete is None:
            raise HTTPException(status_code=404, detail=f"Patient with id {patient_id} does not exist.")

        await self.session.delete(patient_to_delete)
        await self.session.commit()

        return patient_id
