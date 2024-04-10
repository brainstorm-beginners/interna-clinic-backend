from typing import List

from fastapi import APIRouter, Depends

from app.api.v1.services.doctor_service import DoctorService
from app.dependencies import get_doctor_service
from app.schemas.schemas import DoctorRead, DoctorCreateRawPassword, DoctorUpdateRawPassword

router = APIRouter(
    tags=["Doctor"],
    prefix="/api/v1"
)


@router.get("/doctors", response_model=List[DoctorRead])
async def get_doctors(doctor_service: DoctorService = Depends(get_doctor_service), page: int = 1, page_size: int = 10):
    """
    This method is used to retrieve all doctors from the DB with given page and page size.

    Returns:
        doctors (List[PatientRead][start:end])
    """

    doctors = await doctor_service.get_doctors()

    start = (page - 1) * page_size
    end = start + page_size

    return doctors[start:end]


@router.get("/doctors/{doctor_id}", response_model=DoctorRead)
async def get_doctor_by_id(doctor_id: int, doctor_service: DoctorService = Depends(get_doctor_service)):
    """
    This method is used to retrieve a certain doctor from the DB.

    Returns:
        doctor (DoctorRead)
    """

    doctor = await doctor_service.get_doctor_by_id(doctor_id)

    return doctor


# TODO: Move and rename this endpoint to the new 'auth' module as a part of login-registering logic.
@router.post("/doctors/register", response_model=DoctorRead)
async def create_doctor(new_doctor_data: DoctorCreateRawPassword, doctor_service: DoctorService = Depends(get_doctor_service)):
    """
    This method is used to create a doctor with the given data ('DoctorCreateRawPassword' model).

    Returns:
        created doctor (dict[str, Any])
    """

    new_doctor = await doctor_service.create_doctor(new_doctor_data)

    return new_doctor


@router.put("/doctors/{doctor_id}", response_model=DoctorRead)
async def update_doctor(new_data_for_doctor: DoctorUpdateRawPassword, doctor_id: int, doctor_service: DoctorService = Depends(get_doctor_service)):
    """
    This method is used to update the existing doctor data with the new one ('DoctorUpdateRawPassword' model).

    Returns:
        updated doctor (dict[str, Any])
    """

    doctor_to_update = await doctor_service.update_doctor(new_data_for_doctor, doctor_id)

    return doctor_to_update


@router.delete("/doctors/{doctor_id}", response_model=None)
async def delete_doctor(doctor_id: int, doctor_service: DoctorService = Depends(get_doctor_service)) -> dict:
    """
    This method is used to delete the existing doctor with given id.

    Returns:
        deleted doctor ID (int)
    """

    doctor_to_delete = await doctor_service.delete_doctor(doctor_id)

    return doctor_to_delete

