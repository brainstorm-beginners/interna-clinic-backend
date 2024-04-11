from typing import List

from fastapi import APIRouter, Depends

from app.api.v1.services.patient_service import PatientService
from app.dependencies import get_patient_service
from app.schemas.schemas import PatientRead, PatientCreateRawPassword, PatientUpdateRawPassword

router = APIRouter(
    tags=["Patient"],
    prefix="/api/v1"
)


@router.get("/patients", response_model=List[PatientRead])
async def get_patients(patient_service: PatientService = Depends(get_patient_service), page: int = 1, page_size: int = 10):
    """
    This method is used to retrieve all patients from the DB with given page and page size.

    Returns:
        patients (List[PatientRead][start:end])
    """

    patients = await patient_service.get_patients()

    start = (page - 1) * page_size
    end = start + page_size

    return patients[start:end]


@router.get("/patients/{patient_id}", response_model=PatientRead)
async def get_patient_by_id(patient_id: int, patient_service: PatientService = Depends(get_patient_service)):
    """
    This method is used to retrieve a certain patient from the DB.

    Returns:
        patient (PatientRead)
    """

    patient = await patient_service.get_patient_by_id(patient_id)

    return patient


@router.get("/patients/IIN/{patient_IIN}", response_model=PatientRead)
async def get_patient_by_IIN(patient_IIN: str, patient_service: PatientService = Depends(get_patient_service)):
    """
    This method is used to retrieve a certain patient from the DB by his IIN.

    Returns:
        patient (PatientRead)
    """

    patient = await patient_service.get_patient_by_IIN(patient_IIN)

    return patient


# TODO: Move and rename this endpoint to the new 'auth' module as a part of login-registering logic.
@router.post("/patients/register", response_model=PatientRead)
async def create_patient(new_patient_data: PatientCreateRawPassword, patient_service: PatientService = Depends(get_patient_service)):
    """
    This method is used to create a patient with the given data ('PatientCreate' model).

    Returns:
        created patient (dict[str, Any])
    """

    new_patient = await patient_service.create_patient(new_patient_data)

    return new_patient


@router.put("/patients/{patient_id}", response_model=PatientRead)
async def update_patient(patient_id: int, new_data_for_patient: PatientUpdateRawPassword, patient_service: PatientService = Depends(get_patient_service)):
    """
    This method is used to update the existing patient data with the new one ('PatientUpdateRawPassword' model).

    Returns:
        updated patient (dict[str, Any])
    """

    patient_to_update = await patient_service.update_patient(patient_id, new_data_for_patient)

    return patient_to_update


@router.delete("/patients/{patient_id}", response_model=None)
async def delete_patient(patient_id: int, patient_service: PatientService = Depends(get_patient_service)) -> dict:
    """
    This method is used to delete the existing patient with given id.

    Returns:
        A dictionary containing the deleted patient ID and a message (dict)
    """

    result = await patient_service.delete_patient(patient_id)

    return result
