from typing import Sequence, Any, List

from fastapi import HTTPException
from jose import JWTError
from sqlalchemy import select, Row, RowMapping, or_, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.auth import verify_token
from app.models.models import Patient
from app.schemas.schemas import PatientRead, PatientCreateHashedPassword, PatientUpdateHashedPassword


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

    async def get_patient_by_IIN(self, patient_IIN: str) -> PatientRead | None:
        """
        This method is used to retrieve a certain patient from the DB by 'IIN' field.

        Returns:
            patient (PatientRead | None)
        """

        data = await self.session.execute(select(Patient).where(Patient.IIN == patient_IIN))
        patient = data.scalars().first()

        return patient

    async def search_patients(self, search_query: str, token: str) -> Sequence[Row[Any] | RowMapping | Any]:
        """
        This method is used to search patients from the DB by their IIN or name, last name, middle name

        Returns:
            patients (Sequence[Row[Any] | RowMapping | Any])
        """
        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        words = search_query.lower().split()
        conditions = [func.lower(Patient.IIN).like(f"%{word}%") for word in words]
        conditions.extend([func.lower(Patient.first_name).like(f"%{word}%") for word in words])
        conditions.extend([func.lower(Patient.last_name).like(f"%{word}%") for word in words])
        conditions.extend([func.lower(Patient.middle_name).like(f"%{word}%") for word in words])

        query = select(Patient, func.similarity(func.concat_ws(' ', Patient.first_name,
                                                               Patient.last_name, Patient.middle_name),
                                                text(':search_query')).label('similarity')). \
            where(or_(*conditions)). \
            order_by(text('similarity DESC'))

        result = await self.session.execute(query, {'search_query': ' '.join(words)})
        patients = result.scalars().all()

        if not patients:
            raise HTTPException(status_code=404, detail="Patients not found")

        return patients

    async def create_patient(self, new_patient_data: PatientCreateHashedPassword) -> dict[str, Any]:
        """
        This method is used to create a patient with the given data ('PatientCreateHashedPassword' model).

        Returns:
            created patient (dict[str, Any])
        """

        new_patient = Patient(**new_patient_data.model_dump())
        self.session.add(new_patient)
        await self.session.flush()
        await self.session.commit()

        return new_patient

    async def update_patient(self, patient_id: int, new_data_for_patient: PatientUpdateHashedPassword) -> PatientRead:
        """
        This method is used to update the existing patient data with the new one ('PatientUpdateHashedPassword' model).

        Returns:
            updated patient (dict[str, Any])

        Raises:
            HTTPException: If the patient with the given ID is not found.
        """

        patient_to_update = await self.get_patient_by_id(patient_id)

        for key, value in new_data_for_patient.model_dump().items():
            setattr(patient_to_update, key, value)

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

        await self.session.delete(patient_to_delete)
        await self.session.commit()

        return patient_id
