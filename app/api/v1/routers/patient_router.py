from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.auth_router import oauth2_scheme
from app.api.v1.services.pagination.pagination_service import Pagination
from app.api.v1.services.patient_service import PatientService
from app.dependencies import get_patient_service, get_async_session
from app.schemas.schemas import PatientRead, PatientCreateRawPassword, PatientUpdateRawPassword, PatientPaginationResult
from app.api.v1.repositories.patient_repository import PatientRepository

router = APIRouter(
    tags=["Patient"],
    prefix="/api/v1"
)


@router.get("/patients", response_model=PatientPaginationResult)
async def get_patients(token: str = Depends(oauth2_scheme),
                       patient_service: PatientService = Depends(get_patient_service),
                       page: int = 1, page_size: int = 10):
    """
    This method is used to retrieve all patients from the DB with given page and page size.

    Returns:
        patients (PatientPaginationResult)
    """
    pagination = Pagination(page, page_size)
    total, patients = await patient_service.get_patients(token, pagination.offset, page_size)

    return pagination.paginate(total, patients)


@router.get("/patients/{patient_id}", response_model=PatientRead)
async def get_patient_by_id(patient_id: int, token: str = Depends(oauth2_scheme),
                            patient_service: PatientService = Depends(get_patient_service)):
    """
    This method is used to retrieve a certain patient from the DB.

    Returns:
        patient (PatientRead)
    """

    patient = await patient_service.get_patient_by_id(patient_id, token)

    return patient


@router.get("/patients/IIN/{patient_IIN}", response_model=PatientRead)
async def get_patient_by_IIN(patient_IIN: str, token: str = Depends(oauth2_scheme),
                             patient_service: PatientService = Depends(get_patient_service)):
    """
    This method is used to retrieve a certain patient from the DB by his IIN.

    Returns:
        patient (PatientRead)
    """

    patient = await patient_service.get_patient_by_IIN(patient_IIN, token)

    return patient


@router.get("/patients/search/{search_query}", response_model=PatientPaginationResult)
async def search_patients(search_query: str, token: str = Depends(oauth2_scheme),
                          page: int = 1, page_size: int = 10,
                          session: AsyncSession = Depends(get_async_session)):
    """
    This method is used to search and retrieve patients from the DB
    by a search query (any combination of: (first_name, last_name, middle_name) or IIN).

    Returns:
        patients (PatientPaginationResult)
    """
    patient_repository = PatientRepository(session)
    pagination = Pagination(page, page_size)
    total, patients = await patient_repository.search_patients(search_query, token, pagination.offset, page_size)

    return pagination.paginate(total, patients)


@router.post("/patients/register", response_model=PatientRead)
async def create_patient(new_patient_data: PatientCreateRawPassword, token: str = Depends(oauth2_scheme),
                         patient_service: PatientService = Depends(get_patient_service)):
    """
    This method is used to create a patient with the given data ('PatientCreate' model).

    Returns:
        created patient (dict[str, Any])
    """

    new_patient = await patient_service.create_patient(token, new_patient_data)

    return new_patient


@router.put("/patients/{patient_id}", response_model=PatientRead)
async def update_patient(patient_id: int, new_data_for_patient: PatientUpdateRawPassword,
                         token: str = Depends(oauth2_scheme),
                         patient_service: PatientService = Depends(get_patient_service)):
    """
    This method is used to update the existing patient data with the new one ('PatientUpdateRawPassword' model).

    Returns:
        updated patient (dict[str, Any])
    """

    patient_to_update = await patient_service.update_patient(patient_id, token, new_data_for_patient)

    return patient_to_update


@router.delete("/patients/delete/{patient_id}", response_model=None)
async def delete_patient(patient_id: int, token: str = Depends(oauth2_scheme),
                         patient_service: PatientService = Depends(get_patient_service)) -> dict:
    """
    This method is used to delete the existing patient with given id.

    Returns:
        A dictionary containing the deleted patient ID and a message (dict)
    """

    result = await patient_service.delete_patient(patient_id, token)

    return result
