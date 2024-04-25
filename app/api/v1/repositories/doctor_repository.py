from typing import Sequence, Any, Tuple

from fastapi import HTTPException
from jose import JWTError
from sqlalchemy import select, Row, RowMapping, or_, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.auth import verify_token
from app.models.models import Doctor, Patient
from app.schemas.schemas import DoctorRead, DoctorCreateHashedPassword, DoctorUpdateHashedPassword, PatientRead


class DoctorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_doctors_without_pagination(self) -> Sequence[DoctorRead]:
        """
        This method is used to retrieve all doctors from the DB without.

        Returns:
            doctors (Sequence[DoctorRead])
        """

        data = await self.session.execute(select(Doctor))
        doctors = data.scalars().all()

        return doctors

    async def get_doctors(self, offset: int = 0, limit: int = 10) -> Tuple[int, Sequence[DoctorRead]]:
        """
        This method is used to retrieve all doctors from the DB.

        Returns:
            total (int)
            doctors (Sequence[DoctorRead])
        """

        total = await self.session.execute(func.count(Doctor.id))
        total = total.scalar()
        data = await self.session.execute(select(Doctor).offset(offset).limit(limit))
        doctors = data.scalars().all()

        return total, doctors

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

    async def get_doctor_patients(self, doctor_id: int, offset: int = 0, limit: int = 10) -> \
            Tuple[int, Sequence[PatientRead]]:
        """
        Retrieve list of doctor's patients, assigned to the doctor with this ID.

        Arguments:
            doctor_id (int): doctor ID

        Returns:
            total (int)
            Sequence[PatientRead]: List of patients, assigned to the doctor
        """

        total = await self.session.execute(select(func.count(Patient.id)).where(Patient.doctor_id == doctor_id))
        total = total.scalar()
        query = select(Patient).where(Patient.doctor_id == doctor_id).offset(offset).limit(limit)
        data = await self.session.execute(query)
        doctor_patients = data.scalars().all()

        return total, doctor_patients

    async def search_doctors(self, search_query: str, token: str, offset: int = 0, limit: int = 10) -> Sequence[Row[Any] | RowMapping | Any]:
        """
        This method is used to search and retrieve doctors from the DB
        by a search query (any combination of: (first_name, last_name, middle_name) or IIN).

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
            order_by(text('similarity DESC')). \
            offset(offset).limit(limit)

        result = await self.session.execute(query, {'search_query': ' '.join(words)})
        doctors = result.scalars().all()

        total = await self.session.execute(select(func.count()).where(or_(*conditions)))
        total = total.scalar()

        if not doctors:
            raise HTTPException(status_code=404, detail="Doctors not found")

        return total, doctors

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
