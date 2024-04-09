from typing import Sequence, Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Doctor
from app.schemas.schemas import DoctorRead, DoctorCreateHashedPassword, DoctorUpdateHashedPassword


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
        if doctor_to_delete is None:
            raise HTTPException(status_code=404, detail=f"Patient with id {doctor_id} does not exist.")

        await self.session.delete(doctor_to_delete)
        await self.session.commit()

        return doctor_id
