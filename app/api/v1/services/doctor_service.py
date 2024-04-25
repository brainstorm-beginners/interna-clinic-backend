from typing import Any, Sequence, Tuple

from fastapi import HTTPException
from jose import JWTError
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from app.api.v1.auth.auth import verify_token
from app.api.v1.repositories.doctor_repository import DoctorRepository
from app.schemas.schemas import DoctorRead, DoctorCreateRawPassword, DoctorCreateHashedPassword, \
    DoctorUpdateRawPassword, DoctorUpdateHashedPassword, PatientRead, DoctorReadFullName

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


class DoctorService:
    def __init__(self, doctor_repository: DoctorRepository) -> None:
        self.doctor_repository = doctor_repository

    async def get_doctors_without_pagination(self, token: str) -> Sequence[DoctorRead]:
        """
        This method is used to retrieve all doctors from the DB without pagination.

        Returns:
            doctors (Sequence[DoctorRead])
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await self.doctor_repository.get_doctors_without_pagination()

    async def get_doctors(self, token: str, offset: int = 0, page_size: int = 10) -> Tuple[int, Sequence[DoctorRead]]:
        """
        This method is used to retrieve all doctors from the DB.

        Returns:
            total : int
            doctors (Sequence[DoctorRead])
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        total, patients = await self.doctor_repository.get_doctors(offset=offset, limit=page_size)
        return total, patients

    async def get_doctor_by_id(self, doctor_id: int, token: str) -> DoctorRead:
        """
        This method is used to retrieve a certain doctor from the DB by his 'id' field.

        Returns:
            doctor (DoctorRead | None)

        Raises:
            HTTPException (404): if the doctor with given ID does not exist.
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        doctor = await self.doctor_repository.get_doctor_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail=f"Doctor with id {doctor_id} doest not exist.")

        return doctor

    async def get_doctor_by_IIN(self, doctor_IIN: str, token: str) -> DoctorRead | None:
        """
        This method is used to retrieve a certain doctor from the DB by his 'IIN' field.

        Returns:
            doctor (PatientRead | None)
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        doctor = await self.doctor_repository.get_doctor_by_IIN(doctor_IIN)

        if not doctor:
            raise HTTPException(status_code=404, detail=f"Doctor with IIN {doctor_IIN} does not exist.")

        return doctor

    async def get_doctor_full_name_by_id(self, doctor_id: int, token: str) -> DoctorReadFullName | None:
        """
        This method is used to retrieve a certain doctor's full name from the DB by his 'id' field.

        Returns:
            Doctor's full name (DoctorReadFullName | None)

        Raises:
            HTTPException (404): if the doctor with given ID does not exist.
            HTTPException (401): if the token is invalid.
        """

        try:
            verify_token(token)
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        doctor = await self.doctor_repository.get_doctor_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail=f"Doctor with id {doctor_id} doest not exist.")

        doctor_initials = DoctorReadFullName(
            first_name=doctor.first_name,
            last_name=doctor.last_name,
            middle_name=doctor.middle_name,
            qualification=doctor.qualification,
        )

        return doctor_initials

    async def get_doctor_patients(self, doctor_IIN: str, token: str, offset: int = 0, limit: int = 10) -> \
            Tuple[int, Sequence[PatientRead]]:
        """
        Retrieve list of doctor's patients, assigned to the doctor with this IIN.

        Arguments:
            doctor_IIN (str): Doctor's Individual Identification Number
            token (str): User's authentication token

        Returns:
            total (int)
            Sequence[PatientRead]: List of patients (details may be limited due to privacy)
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        existing_doctor = await self.get_doctor_by_IIN(doctor_IIN, token)
        if not existing_doctor:
            raise HTTPException(status_code=404, detail=f"Doctor with IIN {doctor_IIN} does not exist.")

        total, doctor_patients = await self.doctor_repository.get_doctor_patients(existing_doctor.id, offset, limit)
        return total, doctor_patients

    async def create_doctor(self, raw_doctor_data: DoctorCreateRawPassword, token: str) -> dict[str, Any]:
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

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient", "Doctor"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

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

    async def update_doctor(self, new_data_for_doctor: DoctorUpdateRawPassword, doctor_id: int, token: str) -> DoctorRead:
        """
        This method is used to update the existing doctor data with the new one ('DoctorUpdateRawPassword' model).

        Returns:
            updated doctor (DoctorRead)
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        doctor_to_update = await self.doctor_repository.get_doctor_by_id(doctor_id)
        if doctor_to_update is None:
            raise HTTPException(status_code=404, detail=f"Patient with id {doctor_id} does not exist.")

        hashed_password = hash_password(new_data_for_doctor.password)

        doctor_data = new_data_for_doctor.model_dump()
        doctor_data["hashed_password"] = hashed_password
        del doctor_data["password"]

        doctor_with_hashed_password = DoctorUpdateHashedPassword(**doctor_data)

        return await self.doctor_repository.update_doctor(doctor_with_hashed_password, doctor_id)

    async def delete_doctor(self, doctor_id: int, token: str) -> dict:
        """
        This method is used to delete the existing doctor with given id.

        Returns:
            A dictionary containing the deleted doctor ID and a message (dict)

        Raises:
            HTTPException (404): if doctor with given ID does not exist.
            HTTPException (409): if doctor with given ID cannot be deleted because of relationship with
            existing patients.
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

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
