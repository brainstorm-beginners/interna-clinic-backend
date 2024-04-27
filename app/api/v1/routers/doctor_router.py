from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.auth_router import oauth2_scheme
from app.api.v1.repositories.doctor_repository import DoctorRepository
from app.api.v1.services.doctor_service import DoctorService
from app.api.v1.services.pagination.pagination_service import Pagination
from app.dependencies import get_doctor_service, get_async_session
from app.schemas.schemas import DoctorRead, DoctorCreateRawPassword, DoctorUpdateRawPassword, PatientRead, \
    DoctorReadFullName, DoctorPaginationResult, PatientPaginationResult

router = APIRouter(
    tags=["Doctor"],
    prefix="/api/v1"
)


@router.get("/doctors_without_pagination", response_model=List[DoctorRead])
async def get_doctors_without_pagination(token: str = Depends(oauth2_scheme), doctor_service: DoctorService = Depends(get_doctor_service)):
    """
    This method is used to retrieve all doctors from the DB without pagination.

    Returns:
        doctors (List[DoctorRead])
    """

    doctors = await doctor_service.get_doctors_without_pagination(token)

    return doctors


@router.get("/doctors", response_model=DoctorPaginationResult)
async def get_doctors(token: str = Depends(oauth2_scheme), doctor_service: DoctorService = Depends(get_doctor_service),
                      page: int = 1, page_size: int = 10):
    """
    This method is used to retrieve all doctors from the DB with given page and page size.

    Returns:
        doctors (DoctorPaginationResult)
    """

    pagination = Pagination(page, page_size)
    total, doctors = await doctor_service.get_doctors(token, pagination.offset, page_size)

    return pagination.paginate(total, doctors)


@router.get("/doctors/{doctor_id}", response_model=DoctorRead)
async def get_doctor_by_id(doctor_id: int , token: str = Depends(oauth2_scheme),
                           doctor_service: DoctorService = Depends(get_doctor_service)):
    """
    This method is used to retrieve a certain doctor from the DB.

    Returns:
        doctor (DoctorRead)
    """

    doctor = await doctor_service.get_doctor_by_id(doctor_id, token)

    return doctor


@router.get("/doctors/search/{search_query}", response_model=DoctorPaginationResult)
async def search_doctors(search_query: str, token: str = Depends(oauth2_scheme),
                          page: int = 1, page_size: int = 10,
                          session: AsyncSession = Depends(get_async_session)):
    """
    This method is used to search and retrieve doctors from the DB
    by a search query (any combination of: (first_name, last_name, middle_name) or IIN).

    Returns:
        doctors (DoctorPaginationResult)
    """
    doctor_repository = DoctorRepository(session)
    pagination = Pagination(page, page_size)
    total, doctors = await doctor_repository.search_doctors(search_query, token, pagination.offset, page_size)

    return pagination.paginate(total, doctors)


@router.get("/doctors/IIN/{doctor_IIN}", response_model=DoctorRead)
async def get_doctor_by_IIN(doctor_IIN: str, token: str = Depends(oauth2_scheme),
                            doctor_service: DoctorService = Depends(get_doctor_service)):
    """
    This method is used to retrieve a certain doctor from the DB.

    Returns:
        doctor (DoctorRead)
    """

    doctor = await doctor_service.get_doctor_by_IIN(doctor_IIN, token)

    return doctor


@router.get("/doctors/full_name/{doctor_id}", response_model=DoctorReadFullName)
async def get_doctor_full_name_by_id(doctor_id: int, token: str = Depends(oauth2_scheme),
                                     doctor_service: DoctorService = Depends(get_doctor_service)):
    """
    This method is used to retrieve a certain doctor's full name from the DB.

    Returns:
        Doctor's full name (DoctorReadFullName)
    """

    doctor = await doctor_service.get_doctor_full_name_by_id(doctor_id, token)

    return doctor


@router.get("/doctors/{doctor_IIN}/patients", response_model=PatientPaginationResult)
async def get_doctor_patients(doctor_IIN: str, token: str = Depends(oauth2_scheme),
                              doctor_service: DoctorService = Depends(get_doctor_service),
                              page: int = 1, page_size: int = 10):
    """
    This method retrieve list of doctor's patients, assigned to the doctor with this ID.

    Returns:
        List[PatientRead]: List of patients, assigned to the doctor
    """

    pagination = Pagination(page, page_size)
    total, doctor_patients = await doctor_service.get_doctor_patients(doctor_IIN, token, pagination.offset, page_size)

    return pagination.paginate(total, doctor_patients)


# TODO: Move and rename this endpoint to the new 'auth' module as a part of login-registering logic.
@router.post("/doctors/register", response_model=DoctorRead)
async def create_doctor(new_doctor_data: DoctorCreateRawPassword, token: str = Depends(oauth2_scheme),  doctor_service: DoctorService = Depends(get_doctor_service)):
    """
    This method is used to create a doctor with the given data ('DoctorCreateRawPassword' model).

    Returns:
        created doctor (dict[str, Any])
    """

    new_doctor = await doctor_service.create_doctor(new_doctor_data, token)

    return new_doctor


@router.put("/doctors/{doctor_id}", response_model=DoctorRead)
async def update_doctor(new_data_for_doctor: DoctorUpdateRawPassword, doctor_id: int, token: str = Depends(oauth2_scheme),
                        doctor_service: DoctorService = Depends(get_doctor_service)):
    """
    This method is used to update the existing doctor data with the new one ('DoctorUpdateRawPassword' model).

    Returns:
        updated doctor (dict[str, Any])
    """

    doctor_to_update = await doctor_service.update_doctor(new_data_for_doctor, doctor_id, token)

    return doctor_to_update


@router.delete("/doctors/delete/{doctor_id}", response_model=None)
async def delete_doctor(doctor_id: int, token: str = Depends(oauth2_scheme),
                        doctor_service: DoctorService = Depends(get_doctor_service)) -> dict:
    """
    This method is used to delete the existing doctor with given id.

    Returns:
        deleted doctor ID (int)
    """

    doctor_to_delete = await doctor_service.delete_doctor(doctor_id, token)

    return doctor_to_delete

