from typing import Sequence, Any

from fastapi import HTTPException
from jose import JWTError
from sqlalchemy import select, Row, RowMapping, func, text, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.auth import verify_token
from app.models.models import Doctor, Patient
from app.schemas.schemas import DoctorRead, DoctorCreateHashedPassword, DoctorUpdateHashedPassword, PatientRead


class DoctorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_doctors(self) -> Sequence[DoctorRead]:
        """
        This method is used to retrieve all doctors from the DB.

        Returns:
            doctors (Sequence[PatientRead])
        """

        data = await self.session.execute(select(Doctor))
        doctors = data.scalars().all()

        return doctors

    async def get_doctor_by_id(self, doctor_id: int) -> DoctorRead | None:
        """
        This method is used to retrieve a certain doctor from the DB by his 'id' field.

        Returns:
            doctor (Doctor | None)
        """

        data = await self.session.execute(select(Doctor).where(Doctor.id == doctor_id))
        doctor = data.scalars().first()

        return doctor

    async def get_doctor_by_IIN(self, doctor_IIN: str) -> DoctorRead | None:
        """
        This method is used to retrieve a certain doctor from the DB by 'IIN' field.

        Returns:
            doctor (DoctorRead | None)
        """

        data = await self.session.execute(select(Doctor).where(Doctor.IIN == doctor_IIN))
        doctor = data.scalars().first()

        return doctor

    async def get_doctor_patients(self, doctor_id: int) -> Sequence[PatientRead]:
        """
        Retrieve list of doctor's patients, assigned to the doctor with this ID.

        Arguments:
            doctor_id (int): doctor ID

        Returns:
            Sequence[PatientRead]: List of patients, assigned to the doctor
        """

        query = select(Patient).where(Patient.doctor_id == doctor_id)
        data = await self.session.execute(query)
        doctor_patients = data.scalars().all()

        return doctor_patients

    async def search_doctor_by_IIN(self, doctor_IIN: str, token: str) -> Row | RowMapping:
        """
        This method is used to search a certain doctor from the DB by his IIN

        Returns:
            doctor (Row | RowMapping)
        """
        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        query = select(Doctor).where(Doctor.IIN == doctor_IIN)
        result = await self.session.execute(query, {'IIN': doctor_IIN})
        doctor_by_IIN = result.scalars().one_or_none()

        if not doctor_by_IIN:
            raise HTTPException(status_code=404, detail="Doctor not found")

        return doctor_by_IIN

    async def search_doctors(self, search_query: str, token: str) -> Sequence[Row[Any] | RowMapping | Any]:
        """
        This method is used to search doctors from the DB by their IIN or name, last name, middle name

        Returns:
            doctors (Sequence[Row[Any] | RowMapping | Any])
        """
        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        words = search_query.lower().split()
        conditions = [func.lower(Doctor.IIN).like(f"%{word}%") for word in words]
        conditions.extend([func.lower(Doctor.first_name).like(f"%{word}%") for word in words])
        conditions.extend([func.lower(Doctor.last_name).like(f"%{word}%") for word in words])
        conditions.extend([func.lower(Doctor.middle_name).like(f"%{word}%") for word in words])

        query = select(Doctor, func.similarity(func.concat_ws(' ', Doctor.first_name,
                                                               Doctor.last_name, Doctor.middle_name),
                                                text(':search_query')).label('similarity')). \
            where(or_(*conditions)). \
            order_by(text('similarity DESC'))

        result = await self.session.execute(query, {'search_query': ' '.join(words)})
        doctors = result.scalars().all()

        if not doctors:
            raise HTTPException(status_code=404, detail="Patients not found")

        return doctors

    async def create_doctor(self, new_doctor_data: DoctorCreateHashedPassword) -> dict[str, Any]:
        """
        This method is used to create a doctor with the given data ('DoctorCreateHashedPassword' model).

        Returns:
            created doctor (dict[str, Any])
        """

        new_doctor = Doctor(**new_doctor_data.model_dump())
        self.session.add(new_doctor)
        await self.session.flush()
        await self.session.commit()

        return new_doctor

    async def update_doctor(self, new_data_for_doctor: DoctorUpdateHashedPassword, doctor_id: int) -> DoctorRead:
        """
        This method is used to update the existing doctor data with the new one ('DoctorUpdate' model).

        Returns:
            updated doctor (dict[str, Any])

        Raises:
            HTTPException: If the doctor with the given ID is not found.
        """

        doctor_to_update = await self.get_doctor_by_id(doctor_id)

        for key, value in new_data_for_doctor.model_dump().items():
            setattr(doctor_to_update, key, value)

        await self.session.flush()
        await self.session.commit()

        return doctor_to_update

    async def delete_doctor(self, doctor_id: int) -> int:
        """
        This method is used to delete the existing doctor with given ID.

        Returns:
            deleted doctor ID (int)

        Raises:
            HTTPException: If the doctor with the given ID is not found.
        """

        doctor_to_delete = await self.get_doctor_by_id(doctor_id)

        await self.session.delete(doctor_to_delete)
        await self.session.commit()

        return doctor_id
