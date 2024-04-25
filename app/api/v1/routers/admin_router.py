from typing import List

from fastapi import APIRouter, Depends

from app.api.v1.auth.auth_router import oauth2_scheme
from app.api.v1.services.admin_service import AdminService
from app.dependencies import get_admin_service
from app.schemas.schemas import AdminRead, AdminCreateRawPassword, AdminUpdateRawPassword

router = APIRouter(
    tags=["Admins"],
    prefix="/api/v1"
)


@router.get("/admins", response_model=List[AdminRead])
async def get_admins(token: str = Depends(oauth2_scheme), admin_service: AdminService = Depends(get_admin_service)):
    """
    This method is used to retrieve all admins from the DB with given page and page size.

    Returns:
        admins (List[AdminRead])
    """

    admins = await admin_service.get_admins(token)

    return admins


@router.get("/admins/{admin_id}", response_model=AdminRead)
async def get_admin_by_id(admin_id: int, token: str = Depends(oauth2_scheme),
                          admin_service: AdminService = Depends(get_admin_service)):
    """
    This method is used to retrieve a certain admin from the DB.

    Returns:
        admin (AdminRead)
    """

    admin = await admin_service.get_admin_by_id(admin_id, token)

    return admin


# TODO: Move this endpoint to the new 'auth' module as a part of login-registering logic.
@router.post("/admins/register", response_model=AdminRead)
async def register_admin(new_admin_data: AdminCreateRawPassword, token: str = Depends(oauth2_scheme),
                         admin_service: AdminService = Depends(get_admin_service)):
    """
    This method is used to create an admin with the given data ('AdminCreate' model).

    Returns:
        created admin(dict[str, Any])
    """
    new_admin = await admin_service.register_admin(new_admin_data, token)

    return new_admin


@router.put("/admins/{admin_id}", response_model=AdminRead)
async def update_admin(admin_id: int, new_data_for_admin: AdminUpdateRawPassword, token: str = Depends(oauth2_scheme),
                       admin_service: AdminService = Depends(get_admin_service)):
    """
    This method is used to update the existing admin data with the new one ('AdminUpdate' model).

    Returns:
        updated admin (dict[str, Any])
    """

    admin = await admin_service.update_admin(new_data_for_admin, admin_id, token)
    return admin


@router.delete("/admins/delete/{admin_id}", response_model=None)
async def delete_admin(admin_id: int, token: str = Depends(oauth2_scheme),
                       admin_service: AdminService = Depends(get_admin_service)) -> dict:
    """
    This method is used to delete the existing admin with given id.

    Returns:
        deleted admin ID (int)
    """

    admin_to_delete = await admin_service.delete_admin(admin_id, token)

    return admin_to_delete
